from simulator.workload_generator import WorkloadGenerator

from benchmark.runner import BenchmarkRunner
from benchmark.metrics import benchmark_summary
from benchmark.report import print_benchmark_report


from schedulers.fcfs import FCFSScheduler
from schedulers.sjf_oracle import SJFOracleScheduler
from schedulers.priority import PriorityScheduler
from schedulers.round_robin import RoundRobinScheduler
from benchmark.export import (
    save_json,
    save_csv
)


generator = WorkloadGenerator(
    seed=42
)


workload = generator.generate_workload(
    number_of_processes=1000,
    arrival_rate=0.3,
    profile="mixed"
)



runner = BenchmarkRunner(
    workload
)



schedulers = {

    "FCFS":
        FCFSScheduler(),

    "SJF":
        SJFOracleScheduler(),

    "Priority":
        PriorityScheduler(),

    "RoundRobin":
        RoundRobinScheduler(
            quantum=2
        )
}



results = {}



for name, scheduler in schedulers.items():

    print(
        "Running:",
        name
    )


    result = runner.run_scheduler(
        scheduler
    )


    results[name] = benchmark_summary(
        result
    )

print_benchmark_report(
    results
)
save_json(
    results,
    "results/benchmark_seed42.json"
)


save_csv(
    results,
    "results/benchmark_seed42.csv"
)


print(
    "\nResults saved."
)
