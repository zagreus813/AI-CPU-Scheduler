from simulator.process import Process
from simulator.simulator import Simulator

from schedulers.rr_test_scheduler import RRTestScheduler


processes = [

    Process(
        pid="P1",
        arrival_time=0,
        cpu_bursts=[7],
        io_bursts=[]
    ),

    Process(
        pid="P2",
        arrival_time=0,
        cpu_bursts=[4],
        io_bursts=[]
    ),
]


scheduler = RRTestScheduler(
    quantum=2
)


sim = Simulator(
    processes=processes,
    scheduler=scheduler
)


result = sim.run()


print("RESULTS")
print("----------------")

for p in processes:
    print(
        p.pid,
        p.state,
        p.start_time,
        p.finish_time
    )


print("\nTIMELINE")
print("----------------")


for item in result.timeline:
    print(item)
