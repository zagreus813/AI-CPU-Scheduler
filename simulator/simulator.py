import heapq
from typing import List

from simulator.process import Process, ProcessState
from simulator.event import Event, EventType
from simulator.simulation_result import SimulationResult

class Simulator:
    """
    Event-Driven OS Simulator
    """
    def __init__(self, processes: List[Process], scheduler, context_switch_cost: int = 1):
        self.processes = processes
        self.scheduler = scheduler
        self.context_switch_cost = context_switch_cost

        self.current_time = 0
        self.events: List[Event] = []
        
        self.ready_queue: List[Process] = []
        self.blocked_processes: List[Process] = []
        self.running_process: Process = None
        self.cpu_busy: bool = False
        
        self.timeline = []
        
        # Metrics
        self.total_time = 0
        self.cpu_busy_time = 0
        self.cpu_idle_time = 0
        self.context_switch_count = 0
        self.context_switch_time = 0
        
        # Initialization
        self._initialize_events()

    def _initialize_events(self):
        # Reset runtime state for all processes and schedule their arrival
        for process in self.processes:
            process.reset_runtime()
            self._schedule_event(process.arrival_time, EventType.PROCESS_ARRIVAL, process)

    def _schedule_event(self, time: int, event_type: EventType, process: Process):
        event = Event(time=time, event_type=event_type, process=process)
        heapq.heappush(self.events, event)

    def run(self) -> SimulationResult:
        while self.events:
            event = heapq.heappop(self.events)
            
            # Fast-forward time to event time
            if event.time > self.current_time:
                # If CPU was completely idle (not even context switching), record it
                if not self.cpu_busy:
                    self.cpu_idle_time += (event.time - self.current_time)
                self.current_time = event.time
                
            if event.event_type == EventType.PROCESS_ARRIVAL:
                self._handle_process_arrival(event.process)
            elif event.event_type == EventType.PROCESS_DISPATCH:
                self._handle_process_dispatch(event.process)
            elif event.event_type == EventType.QUANTUM_EXPIRE:
                self._handle_quantum_expire(event.process)
            elif event.event_type == EventType.CPU_BURST_COMPLETE:
                self._handle_cpu_burst_complete(event.process)
            elif event.event_type == EventType.IO_COMPLETE:
                self._handle_io_complete(event.process)

        self.total_time = self.current_time

        return SimulationResult(
            processes=self.processes,
            timeline=self.timeline,
            total_time=self.total_time,
            cpu_busy_time=self.cpu_busy_time,
            cpu_idle_time=self.cpu_idle_time,
            context_switch_count=self.context_switch_count,
            context_switch_time=self.context_switch_time
        )

    def _handle_process_arrival(self, process: Process):
        process.mark_ready(self.current_time)
        self.ready_queue.append(process)
        
        self._invoke_scheduler()

    def _handle_process_dispatch(self, process: Process):
        if self.running_process is not None:
            raise RuntimeError("Cannot dispatch a process when CPU is already running a process.")

        self.running_process = process
        process.start_running(self.current_time)
        
        # Check if the scheduler set a quantum for preemption
        quantum = getattr(self.scheduler, 'current_quantum', None)

        if quantum is not None and process.remaining_cpu_time > quantum:
            # Preemption event
            self._schedule_event(self.current_time + quantum, EventType.QUANTUM_EXPIRE, process)
        else:
            # Burst complete event
            self._schedule_event(self.current_time + process.remaining_cpu_time, EventType.CPU_BURST_COMPLETE, process)

    def _handle_quantum_expire(self, process: Process):
        # Determine actual execution time
        quantum = getattr(self.scheduler, 'current_quantum')
        
        process.run_for(quantum)
        self.cpu_busy_time += quantum
        
        # Record timeline
        self.timeline.append({
            "pid": process.pid,
            "start": self.current_time - quantum,
            "end": self.current_time,
            "event": "CPU"
        })

        process.preempt(self.current_time)
        self.running_process = None
        self.cpu_busy = False
        self.ready_queue.append(process)
        
        self._invoke_scheduler()

    def _handle_cpu_burst_complete(self, process: Process):
        execution_time = process.remaining_cpu_time
        process.run_for(execution_time)
        self.cpu_busy_time += execution_time
        
        # Record timeline
        self.timeline.append({
            "pid": process.pid,
            "start": self.current_time - execution_time,
            "end": self.current_time,
            "event": "CPU"
        })

        io_burst = process.complete_cpu_burst()
        self.running_process = None
        self.cpu_busy = False

        if io_burst is not None:
            self.blocked_processes.append(process)
            self._schedule_event(self.current_time + io_burst, EventType.IO_COMPLETE, process)
        else:
            process.terminate(self.current_time)
            
        self._invoke_scheduler()

    def _handle_io_complete(self, process: Process):
        self.blocked_processes.remove(process)
        process.complete_io(self.current_time)
        self.ready_queue.append(process)
        
        self._invoke_scheduler()

    def _invoke_scheduler(self):
        if self.cpu_busy:
            return  # CPU is busy (either running or context switching)

        if not self.ready_queue:
            return  # No process to schedule

        # Let the scheduler select the next process
        selected_process = self.scheduler.select_process(self.ready_queue, self.current_time)

        if selected_process:
            self.ready_queue.remove(selected_process)
            self.cpu_busy = True
            
            dispatch_time = self.current_time
            
            # Apply context switch overhead
            if self.context_switch_cost > 0:
                self.context_switch_count += 1
                self.context_switch_time += self.context_switch_cost
                
                # Context switch consumes time
                dispatch_time = self.current_time + self.context_switch_cost
                
                self.timeline.append({
                    "pid": "CONTEXT_SWITCH",
                    "start": self.current_time,
                    "end": dispatch_time,
                    "event": "CONTEXT_SWITCH"
                })
                selected_process.record_context_switch()

            self._schedule_event(dispatch_time, EventType.PROCESS_DISPATCH, selected_process)
