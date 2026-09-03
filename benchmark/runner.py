from simulator.simulator import Simulator


class BenchmarkRunner:


    def __init__(
        self,
        workload
    ):
        self.workload = workload



    def run_scheduler(
        self,
        scheduler
    ):

        processes = [
            p.clone()
            for p in self.workload
        ]


        simulator = Simulator(
            processes=processes,
            scheduler=scheduler
        )


        result = simulator.run()


        return result
