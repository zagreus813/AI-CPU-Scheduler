from collections import deque


def round_robin(processes, quantum=2):

    processes = sorted(
        processes,
        key=lambda p: p.arrival_time
    )

    ready_queue = deque()

    current_time = 0
    index = 0

    completed = []
    timeline = []

    while len(completed) < len(processes):

        while (
            index < len(processes)
            and
            processes[index].arrival_time <= current_time
        ):
            ready_queue.append(
                processes[index]
            )
            index += 1

        if not ready_queue:

            if index < len(processes):
                current_time = (
                    processes[index].arrival_time
                )
                continue

            break

        process = ready_queue.popleft()

        if process.start_time is None:
            process.start_time = current_time

        execution_time = min(
            quantum,
            process.remaining_time
        )

        start = current_time

        current_time += execution_time

        process.remaining_time -= (
            execution_time
        )

        end = current_time

        timeline.append(
            (process.pid, start, end)
        )

        while (
            index < len(processes)
            and
            processes[index].arrival_time <= current_time
        ):
            ready_queue.append(
                processes[index]
            )
            index += 1

        if process.remaining_time == 0:

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

        else:
            ready_queue.append(process)

    return completed, timeline
