from schedulers.base import BaseScheduler


class PriorityScheduler(BaseScheduler):

    def select_process(
        self,
        ready_queue,
        current_time,
        system_state=None
    ):

        if not ready_queue:
            return None


        return min(
            ready_queue,
            key=lambda p: (
                p.priority,
                p.ready_since
            )
        )
