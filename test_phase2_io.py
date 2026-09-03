from simulator.process import Process
from simulator.simulator import Simulator
from schedulers.test_scheduler import TestScheduler


process = Process(
    pid="P1",
    arrival_time=0,
    cpu_bursts=[
        5,
        3
    ],
    io_bursts=[
        10
    ],
)


sim = Simulator(
    processes=[process],
    scheduler=TestScheduler()
)


result = sim.run()


print("STATE")
print(process.state)


print("\nCPU HISTORY")
print(process.cpu_history)


print("\nIO HISTORY")
print(process.io_history)


print("\nTIMES")

print(
    "start:",
    process.start_time
)

print(
    "finish:",
    process.finish_time
)

print(
    "turnaround:",
    process.turnaround_time
)


print("\nTIMELINE")

for item in result.timeline:
    print(item)
