from simulator.process import Process

from schedulers.fcfs import fcfs
from schedulers.sjf import sjf
from schedulers.round_robin import round_robin


def create_processes():
    return [
        Process("P1", arrival_time=0, burst_time=8),
        Process("P2", arrival_time=1, burst_time=4),
        Process("P3", arrival_time=2, burst_time=9),
        Process("P4", arrival_time=3, burst_time=5),
    ]


def print_results(processes, scheduler_name):
    print(f"\n{scheduler_name} Scheduling Results")
    print("-" * 70)

    print(
        f"{'PID':<8}"
        f"{'Arrival':<12}"
        f"{'Burst':<10}"
        f"{'Waiting':<12}"
        f"{'Turnaround':<15}"
        f"{'Response':<10}"
    )

    print("-" * 70)

    for p in processes:
        print(
            f"{p.pid:<8}"
            f"{p.arrival_time:<12}"
            f"{p.burst_time:<10}"
            f"{p.waiting_time:<12}"
            f"{p.turnaround_time:<15}"
            f"{p.response_time:<10}"
        )


def calculate_average_metrics(processes):
    if not processes:
        return 0, 0, 0

    n = len(processes)

    avg_waiting = sum(
        p.waiting_time for p in processes
    ) / n

    avg_turnaround = sum(
        p.turnaround_time for p in processes
    ) / n

    avg_response = sum(
        p.response_time for p in processes
    ) / n

    print("\nAverage Metrics")
    print("-" * 30)

    print(
        f"Average Waiting Time    : "
        f"{avg_waiting:.2f}"
    )

    print(
        f"Average Turnaround Time : "
        f"{avg_turnaround:.2f}"
    )

    print(
        f"Average Response Time   : "
        f"{avg_response:.2f}"
    )

    return (
        avg_waiting,
        avg_turnaround,
        avg_response,
    )


def print_timeline(timeline, scheduler_name):
    print(f"\n{scheduler_name} Timeline")
    print("-" * 50)

    for pid, start, end in timeline:
        print(
            f"{pid:<5}: "
            f"{start:<3} -> {end:<3}"
        )


def print_comparison(
    fcfs_metrics,
    sjf_metrics,
    rr_metrics
):
    print("\nScheduler Comparison")
    print("-" * 65)

    print(
        f"{'Scheduler':<15}"
        f"{'Waiting':<15}"
        f"{'Turnaround':<15}"
        f"{'Response':<15}"
    )

    print("-" * 65)

    print(
        f"{'FCFS':<15}"
        f"{fcfs_metrics[0]:<15.2f}"
        f"{fcfs_metrics[1]:<15.2f}"
        f"{fcfs_metrics[2]:<15.2f}"
    )

    print(
        f"{'SJF':<15}"
        f"{sjf_metrics[0]:<15.2f}"
        f"{sjf_metrics[1]:<15.2f}"
        f"{sjf_metrics[2]:<15.2f}"
    )

    print(
        f"{'Round Robin':<15}"
        f"{rr_metrics[0]:<15.2f}"
        f"{rr_metrics[1]:<15.2f}"
        f"{rr_metrics[2]:<15.2f}"
    )


def main():
    # ==========================================
    # FCFS
    # ==========================================

    fcfs_processes = create_processes()

    fcfs_results, fcfs_timeline = fcfs(
        fcfs_processes
    )

    print_results(
        fcfs_results,
        "FCFS"
    )

    fcfs_metrics = calculate_average_metrics(
        fcfs_results
    )

    print_timeline(
        fcfs_timeline,
        "FCFS"
    )

    # ==========================================
    # SJF
    # ==========================================

    sjf_processes = create_processes()

    sjf_results, sjf_timeline = sjf(
        sjf_processes
    )

    print_results(
        sjf_results,
        "SJF"
    )

    sjf_metrics = calculate_average_metrics(
        sjf_results
    )

    print_timeline(
        sjf_timeline,
        "SJF"
    )

    # ==========================================
    # ROUND ROBIN
    # ==========================================

    rr_processes = create_processes()

    rr_results, rr_timeline = round_robin(
        rr_processes,
        quantum=2
    )

    print_results(
        rr_results,
        "Round Robin"
    )

    rr_metrics = calculate_average_metrics(
        rr_results
    )

    print_timeline(
        rr_timeline,
        "Round Robin"
    )

    # ==========================================
    # COMPARISON
    # ==========================================

    print_comparison(
        fcfs_metrics,
        sjf_metrics,
        rr_metrics
    )


if __name__ == "__main__":
    main()
