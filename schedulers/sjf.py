def sjf(processes):
    processes = sorted(
        processes,
        key=lambda p: p.arrival_time
    )

    current_time = 0
    completed = []
    remaining = processes.copy()

    timeline = []

    while remaining:

        available = [
            p for p in remaining
            if p.arrival_time <= current_time
        ]

        if not available:
            current_time = min(
                p.arrival_time
                for p in remaining
            )
            continue

        process = min(
            available,
            key=lambda p: p.burst_time
        )

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

        completed.append(process)
        remaining.remove(process)

    return completed, timeline
