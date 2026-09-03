def average_waiting_time(processes):

    values = [
        p.waiting_time
        for p in processes
        if p.waiting_time is not None
    ]

    if not values:
        return 0

    return sum(values) / len(values)



def average_turnaround_time(processes):

    values = [
        p.turnaround_time
        for p in processes
        if p.turnaround_time is not None
    ]

    if not values:
        return 0

    return sum(values) / len(values)



def average_response_time(processes):

    values = [
        p.response_time
        for p in processes
        if p.response_time is not None
    ]

    if not values:
        return 0

    return sum(values) / len(values)



def cpu_utilization(result):

    if result.total_time == 0:
        return 0


    return (
        result.cpu_busy_time
        /
        result.total_time
    )



def throughput(result):

    if result.total_time == 0:
        return 0


    return (
        len(result.processes)
        /
        result.total_time
    )



def context_switches(result):

    return result.context_switch_count



def context_switch_overhead(result):

    return result.context_switch_time


def context_switch_ratio(result):

    if result.total_time == 0:
        return 0


    return (
        result.context_switch_time
        /
        result.total_time
    )

def benchmark_summary(result):

    return {

        "waiting":
            average_waiting_time(
                result.processes
            ),


        "turnaround":
            average_turnaround_time(
                result.processes
            ),


        "response":
            average_response_time(
                result.processes
            ),


        "cpu_utilization":
            cpu_utilization(
                result
            ),


        "throughput":
            throughput(
                result
            ),


        "context_switches":
            context_switches(
                result
            ),


        "context_switch_overhead":
            context_switch_overhead(
                result
            ),
        "context_switch_ratio":
            context_switch_ratio(
            result
            )
    }
