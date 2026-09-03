from simulator.process import Process

from schedulers.fcfs import FCFSScheduler
from schedulers.sjf_oracle import SJFOracleScheduler
from schedulers.priority import PriorityScheduler


processes = [

    Process(
        "P1",
        0,
        cpu_bursts=[8]
    ),

    Process(
        "P2",
        0,
        cpu_bursts=[3]
    ),

    Process(
        "P3",
        0,
        cpu_bursts=[5]
    )

]


for p in processes:
    p.mark_ready(0)


print(
    "FCFS:",
    FCFSScheduler()
    .select_process(
        processes,
        0
    )
)


print(
    "SJF:",
    SJFOracleScheduler()
    .select_process(
        processes,
        0
    )
)


print(
    "Priority:",
    PriorityScheduler()
    .select_process(
        processes,
        0
    )
)
