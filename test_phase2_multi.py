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

    Process(
        pid="P2",
        arrival_time=2,
        cpu_bursts=[3],
        io_bursts=[]
    ),

    Process(
        pid="P3",
        arrival_time=4,
        cpu_bursts=[4],
        io_bursts=[]
    ),
]


sim = Simulator(
    processes=processes,
    scheduler=TestScheduler()
)


result = sim.run()


print("PROCESS RESULTS")
print("----------------")


for p in processes:

    print(
        p.pid,
        p.state,
        "start=",
        p.start_time,
        "finish=",
        p.finish_time
    )


print("\nTIMELINE")
print("----------------")


for item in result.timeline:
    print(item)


print("\nMETRICS")
print("----------------")

print(
    "total:",
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

print(
    "context switches:",
    result.context_switch_count
)
