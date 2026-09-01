def fcfs(processes):
    processes = sorted(
        processes,
        key=lambda p: p.arrival_time
    )

    current_time = 0
    timeline = []

    for process in processes:

        if current_time < process.arrival_time:
            current_time = process.arrival_time

        process.start_time = current_time

        start = current_time

        current_time += process.burst_time

        end = current_time

        timeline.append(
            (process.pid, start, end)
        )

        process.finish_time = current_time

        process.turnaround_time = (
            process.finish_time
            - process.arrival_time
        )

        process.waiting_time = (
            process.turnaround_time
            - process.burst_time
        )

        process.response_time = (
            process.start_time
            - process.arrival_time
        )

    return processes, timeline
