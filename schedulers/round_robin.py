from collections import deque

from schedulers.base import BaseScheduler


class RoundRobinScheduler(BaseScheduler):

    def __init__(self, quantum=2):
        self.quantum = quantum

        # Simulator reads this
        self.current_quantum = quantum

        self.queue = deque()


    def select_process(
        self,
        ready_queue,
        current_time,
        system_state=None
    ):

        if not ready_queue:
            return None


        # Add new processes
        for process in ready_queue:

            if process not in self.queue:
                self.queue.append(process)


        # Remove terminated/not-ready processes
        self.queue = deque(
            [
                p
                for p in self.queue
                if p in ready_queue
            ]
        )


        if not self.queue:
            return None


        process = self.queue.popleft()

        return process


    def on_process_end(
        self,
        process,
        current_time
    ):

        pass
