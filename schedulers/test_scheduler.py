class TestScheduler:

    def select_process(
        self,
        ready_queue,
        current_time
    ):
        return ready_queue[0]
