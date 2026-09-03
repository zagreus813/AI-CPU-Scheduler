def print_benchmark_report(results):

    print("\n")
    print("=" * 100)
    print("Scheduler Benchmark Results")
    print("=" * 100)


    header = (
        "Scheduler".ljust(15)
        +
        "Waiting".ljust(14)
        +
        "Turnaround".ljust(14)
        +
        "Response".ljust(14)
        +
        "CPU Util".ljust(14)
        +
        "Throughput".ljust(14)
        +
        "Context".ljust(10)
    )


    print(header)
    print("-" * 100)


    for name, m in results.items():

        print(
            name.ljust(15)
            +
            f"{m['waiting']:.2f}".ljust(14)
            +
            f"{m['turnaround']:.2f}".ljust(14)
            +
            f"{m['response']:.2f}".ljust(14)
            +
            f"{m['cpu_utilization']*100:.2f}%".ljust(14)
            +
            f"{m['throughput']:.4f}".ljust(14)
            +
            f"{m['context_switches']}".ljust(10)
        )
