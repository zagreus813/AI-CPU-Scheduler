from simulator.process import Process
from simulator.simulator import Simulator

from schedulers.fcfs import FCFSScheduler
from schedulers.sjf_oracle import SJFOracleScheduler


def run(name, scheduler):

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
            arrival_time=0,
            cpu_bursts=[3],
            io_bursts=[]
        ),

        Process(
            pid="P3",
            arrival_time=0,
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
        if item["event"] == "CPU":
            print(
                item["pid"],
                item["start"],
                item["end"]
            )


run(
    "FCFS",
    FCFSScheduler()
)


run(
    "SJF Oracle",
    SJFOracleScheduler()
)
