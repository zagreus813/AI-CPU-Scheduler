from simulator.process import Process

from schedulers.round_robin import (
    RoundRobinScheduler
)


processes = [

    Process(
        "P1",
        0,
        cpu_bursts=[8]
    ),

    Process(
        "P2",
        0,
        cpu_bursts=[4]
    )

]


for p in processes:
    p.mark_ready(0)


scheduler = RoundRobinScheduler(
    quantum=2
)


print(
    scheduler.current_quantum
)


print(
    scheduler.select_process(
        processes,
        0
    )
)


print(
    scheduler.select_process(
        processes,
        0
    )
)
