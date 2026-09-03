from abc import ABC, abstractmethod


class BaseScheduler(ABC):
    """
    Base interface for all schedulers.

    Scheduler responsibility:
        ONLY select next process.

    Scheduler must NOT:
        - modify process state
        - advance time
        - execute CPU
        - handle I/O
    """


    @abstractmethod
    def select_process(
        self,
        ready_queue,
        current_time,
        system_state=None
    ):
        """
        Select next process from ready queue.

        Returns:
            Process object
            or None
        """

        pass


    def on_process_start(
        self,
        process,
        current_time
    ):
        """
        Optional hook.

        Called when scheduler's selected
        process starts running.
        """

        pass


    def on_process_end(
        self,
        process,
        current_time
    ):
        """
        Optional hook.

        Called after process finishes CPU burst.
        """

        pass
