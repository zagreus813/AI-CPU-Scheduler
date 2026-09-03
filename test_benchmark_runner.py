from simulator.workload_generator import WorkloadGenerator

from benchmark.runner import BenchmarkRunner

from schedulers.fcfs import FCFSScheduler



generator = WorkloadGenerator(
    seed=42
)


workload = generator.generate_workload(
    number_of_processes=100,
    arrival_rate=0.3,
    profile="mixed"
)


runner = BenchmarkRunner(
    workload
)


result = runner.run_scheduler(
    FCFSScheduler()
)


print(
    "Processes:",
    len(result.processes)
)


print(
    "Total time:",
    result.total_time
)


print(
    "Busy:",
    result.cpu_busy_time
)


print(
    "Context:",
    result.context_switch_count
)
