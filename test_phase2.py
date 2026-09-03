import pytest
from simulator.process import Process, ProcessState
from simulator.simulator import Simulator
from simulator.workload_generator import WorkloadGenerator

class MockFCFSScheduler:
    def select_process(self, ready_queue, current_time, system_state=None):
        if not ready_queue:
            return None
        # FCFS logic: return the process that arrived first (or has been ready longest)
        # Using arrival time for simplicity in these tests
        return min(ready_queue, key=lambda p: (p.arrival_time, p.pid))

class MockRRScheduler:
    def __init__(self, quantum):
        self.current_quantum = quantum
        
    def select_process(self, ready_queue, current_time, system_state=None):
        if not ready_queue:
            return None
        # Simple pop(0) for RR
        return ready_queue[0]

def test_single_process():
    p1 = Process(pid="P1", arrival_time=0, cpu_bursts=[5])
    scheduler = MockFCFSScheduler()
    sim = Simulator([p1], scheduler, context_switch_cost=0)
    
    result = sim.run()
    
    assert p1.state == ProcessState.TERMINATED
    assert result.total_time == 5
    assert result.cpu_busy_time == 5
    assert result.cpu_idle_time == 0
    
    assert len(result.timeline) == 1
    assert result.timeline[0] == {"pid": "P1", "start": 0, "end": 5, "event": "CPU"}

def test_cpu_idle_before_arrival():
    p1 = Process(pid="P1", arrival_time=10, cpu_bursts=[5])
    scheduler = MockFCFSScheduler()
    sim = Simulator([p1], scheduler, context_switch_cost=0)
    
    result = sim.run()
    
    assert p1.state == ProcessState.TERMINATED
    assert result.total_time == 15
    assert result.cpu_busy_time == 5
    assert result.cpu_idle_time == 10
    
    assert len(result.timeline) == 1
    assert result.timeline[0] == {"pid": "P1", "start": 10, "end": 15, "event": "CPU"}

def test_cpu_and_io():
    p1 = Process(pid="P1", arrival_time=0, cpu_bursts=[5, 3], io_bursts=[10])
    scheduler = MockFCFSScheduler()
    sim = Simulator([p1], scheduler, context_switch_cost=0)
    
    result = sim.run()
    
    assert p1.state == ProcessState.TERMINATED
    assert result.total_time == 18 # 5 (CPU) + 10 (IO) + 3 (CPU)
    assert result.cpu_busy_time == 8
    assert result.cpu_idle_time == 10
    
    assert len(result.timeline) == 2
    assert result.timeline[0] == {"pid": "P1", "start": 0, "end": 5, "event": "CPU"}
    assert result.timeline[1] == {"pid": "P1", "start": 15, "end": 18, "event": "CPU"}

def test_multiple_processes():
    p1 = Process(pid="P1", arrival_time=0, cpu_bursts=[5])
    p2 = Process(pid="P2", arrival_time=2, cpu_bursts=[4])
    p3 = Process(pid="P3", arrival_time=10, cpu_bursts=[3])
    
    scheduler = MockFCFSScheduler()
    sim = Simulator([p1, p2, p3], scheduler, context_switch_cost=0)
    
    result = sim.run()
    
    assert p1.state == ProcessState.TERMINATED
    assert p2.state == ProcessState.TERMINATED
    assert p3.state == ProcessState.TERMINATED
    
    assert result.total_time == 13 # P1 finishes at 5, P2 at 9, P3 arrives at 10 and finishes at 13
    assert result.cpu_busy_time == 12
    assert result.cpu_idle_time == 1 # Time 9 to 10
    assert result.context_switch_count == 0

def test_concurrent_io():
    p1 = Process(pid="P1", arrival_time=0, cpu_bursts=[2, 2], io_bursts=[10])
    p2 = Process(pid="P2", arrival_time=0, cpu_bursts=[3, 3], io_bursts=[10])
    
    scheduler = MockFCFSScheduler()
    sim = Simulator([p1, p2], scheduler, context_switch_cost=0)
    
    result = sim.run()
    
    # Timeline:
    # 0 -> 2: P1 CPU (then blocks until 12)
    # 2 -> 5: P2 CPU (then blocks until 15)
    # 5 -> 12: Idle (7 units)
    # 12 -> 14: P1 CPU (terminates)
    # 14 -> 15: Idle (1 unit)
    # 15 -> 18: P2 CPU (terminates)
    
    assert p1.state == ProcessState.TERMINATED
    assert p2.state == ProcessState.TERMINATED
    assert result.total_time == 18
    assert result.cpu_busy_time == 10
    assert result.cpu_idle_time == 8

def test_context_switch():
    p1 = Process(pid="P1", arrival_time=0, cpu_bursts=[5])
    p2 = Process(pid="P2", arrival_time=1, cpu_bursts=[5])
    
    scheduler = MockFCFSScheduler()
    # P1 dispatched at 0, costs 1 CS, runs 1 -> 6
    # P2 dispatched at 6, costs 1 CS, runs 7 -> 12
    sim = Simulator([p1, p2], scheduler, context_switch_cost=1)
    
    result = sim.run()
    
    assert result.total_time == 12
    assert result.context_switch_count == 2
    assert result.context_switch_time == 2
    assert result.cpu_busy_time == 10

def test_preemption():
    # P1 burst = 10, quantum = 4
    p1 = Process(pid="P1", arrival_time=0, cpu_bursts=[10])
    
    scheduler = MockRRScheduler(quantum=4)
    sim = Simulator([p1], scheduler, context_switch_cost=0)
    
    result = sim.run()
    
    # 0 -> 4, preempt
    # 4 -> 8, preempt
    # 8 -> 10, terminate
    
    assert result.total_time == 10
    assert result.cpu_busy_time == 10
    assert len(result.timeline) == 3
    
    assert result.timeline[0] == {"pid": "P1", "start": 0, "end": 4, "event": "CPU"}
    assert result.timeline[1] == {"pid": "P1", "start": 4, "end": 8, "event": "CPU"}
    assert result.timeline[2] == {"pid": "P1", "start": 8, "end": 10, "event": "CPU"}

def test_large_workload():
    generator = WorkloadGenerator(seed=42)
    processes = generator.generate_workload(
        number_of_processes=10000,
        arrival_rate=0.3,
        profile="mixed",
    )
    
    scheduler = MockFCFSScheduler()
    sim = Simulator(processes, scheduler, context_switch_cost=1)
    
    result = sim.run()
    
    # Verify all processes terminated
    for p in processes:
        assert p.state == ProcessState.TERMINATED
        
    assert result.total_time > 0
    assert result.cpu_busy_time > 0
