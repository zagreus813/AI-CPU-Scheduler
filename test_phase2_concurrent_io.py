from simulator.process import Process
from simulator.simulator import Simulator
from schedulers.test_scheduler import TestScheduler


processes = [

    Process(
        pid="P1",
        arrival_time=0,
        cpu_bursts=[
            3,
            2
        ],
        io_bursts=[
            10
        ],
    ),

    Process(
        pid="P2",
        arrival_time=1,
        cpu_bursts=[
            4,
            2
        ],
        io_bursts=[
            5
        ],
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
        p.finish_time,
        "cpu=",
        p.cpu_history,
        "io=",
        p.io_history
    )


print("\nTIMELINE")
print("----------------")

for item in result.timeline:
    print(item)


print("\nMETRICS")
print("----------------")

print("total:", result.total_time)
print("busy:", result.cpu_busy_time)
print("idle:", result.cpu_idle_time)
print(
    "context:",
    result.context_switch_count
)
