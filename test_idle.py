from simulator.process import Process
from simulator.simulator import Simulator


p = Process(
    pid="P1",
    arrival_time=10,
    cpu_bursts=[5],
    io_bursts=[],
)


sim = Simulator(
    processes=[p]
)


result = sim.run()


print("Total time:",
      result.total_time)

print("Idle time:",
      result.cpu_idle_time)

print(result.timeline)
