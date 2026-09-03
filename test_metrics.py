from benchmark.metrics import *


class DummyProcess:

    def __init__(
        self,
        waiting,
        turnaround,
        response
    ):
        self.waiting_time = waiting
        self.turnaround_time = turnaround
        self.response_time = response



processes = [

    DummyProcess(5,10,2),

    DummyProcess(3,8,1)

]


print(
    "waiting:",
    average_waiting_time(processes)
)


print(
    "turnaround:",
    average_turnaround_time(processes)
)


print(
    "response:",
    average_response_time(processes)
)
