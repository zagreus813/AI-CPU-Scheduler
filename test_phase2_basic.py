from simulator.process import Process
from simulator.simulator import Simulator


def main():

    p = Process(
        pid="P1",
        arrival_time=0,
        cpu_bursts=[5],
        io_bursts=[],
        priority=1,
        process_type="cpu_bound",
    )

    sim = Simulator(
        processes=[p]
    )

    result = sim.run()

    print("Simulation finished")

    print("Process state:")
    print(p.state)

    print("Start:")
    print(p.start_time)

    print("Finish:")
    print(p.finish_time)

    print("Turnaround:")
    print(p.turnaround_time)

    print("Timeline:")
    for item in result.timeline:
        print(item)


if __name__ == "__main__":
    main()
