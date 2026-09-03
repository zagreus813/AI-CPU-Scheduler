class RRTestScheduler:

    def __init__(self, quantum=2):
        self.current_quantum = quantum


    def select_process(
        self,
        ready_queue,
        current_time
    ):
        return ready_queue[0]
