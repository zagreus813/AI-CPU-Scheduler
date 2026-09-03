from simulator.process import Process
from simulator.simulator import Simulator
from schedulers.test_scheduler import TestScheduler


processes = [

    Process(
        pid="P1",
        arrival_time=0,
        cpu_bursts=[5],
        io_bursts=[]
    ),

]


scheduler = TestScheduler()


sim = Simulator(
    processes=processes,
    scheduler=scheduler
)


result = sim.run()


print("STATE")
print(processes[0].state)


print("\nTIMES")

print(
    "start:",
    processes[0].start_time
)

print(
    "finish:",
    processes[0].finish_time
)


print("\nRESULT")

print(
    "total time:",
    result.total_time
)


print(
    "busy:",
    result.cpu_busy_time
)


print(
    "idle:",
    result.cpu_idle_time
)


print("\nTIMELINE")

for item in result.timeline:
    print(item)
