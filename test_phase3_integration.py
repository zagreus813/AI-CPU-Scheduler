from simulator.process import Process
from simulator.simulator import Simulator

from schedulers.fcfs import FCFSScheduler
from schedulers.sjf_oracle import SJFOracleScheduler
from schedulers.priority import PriorityScheduler


def run_test(name, scheduler):

    print("\n================")
    print(name)
    print("================")


    processes = [

        Process(
            pid="P1",
            arrival_time=0,
            cpu_bursts=[8],
            io_bursts=[]
        ),

        Process(
            pid="P2",
            arrival_time=1,
            cpu_bursts=[3],
            io_bursts=[]
        ),

        Process(
            pid="P3",
            arrival_time=2,
            cpu_bursts=[5],
            io_bursts=[]
        ),

    ]


    sim = Simulator(
        processes=processes,
        scheduler=scheduler
    )


    result = sim.run()


    for item in result.timeline:
        print(item)


    print("\nMetrics")
    print(
        "total:",
        result.total_time
    )

    print(
        "busy:",
        result.cpu_busy_time
    )


run_test(
    "FCFS",
    FCFSScheduler()
)


run_test(
    "SJF Oracle",
    SJFOracleScheduler()
)


run_test(
    "Priority",
    PriorityScheduler()
)
