from enum import Enum


class ProcessState(str, Enum):
    NEW = "NEW"
    READY = "READY"
    RUNNING = "RUNNING"
    BLOCKED = "BLOCKED"
    TERMINATED = "TERMINATED"


class Process:
    def __init__(
        self,
        pid,
        arrival_time,
        cpu_bursts=None,
        io_bursts=None,
        priority=5,
        process_type="generic",
        burst_time=None,
    ):
        """
        Process model for the OS simulator.

        Parameters
        ----------
        pid:
            Unique process identifier.

        arrival_time:
            Time at which the process enters the system.

        cpu_bursts:
            List of CPU bursts.
            Example: [5, 3, 8]

        io_bursts:
            List of I/O bursts between CPU bursts.
            Example: [20, 15]

            Rule:
            len(io_bursts) == len(cpu_bursts) - 1

        priority:
            Lower number = higher priority.

        process_type:
            interactive / io_bound / cpu_bound / batch / generic

        burst_time:
            Backward compatibility with Phase 0.
            Example:
            Process("P1", 0, burst_time=8)
        """

        # ------------------------------------------
        # Backward compatibility
        # ------------------------------------------

        if cpu_bursts is None:
            if burst_time is None:
                raise ValueError(
                    "cpu_bursts or burst_time must be provided"
                )

            cpu_bursts = [burst_time]

        elif burst_time is not None:
            raise ValueError(
                "Use either cpu_bursts or burst_time, not both"
            )

        if io_bursts is None:
            io_bursts = []

        # ------------------------------------------
        # Normalize values
        # ------------------------------------------

        self.pid = str(pid)
        self.arrival_time = int(arrival_time)

        self.cpu_bursts = [
            int(value)
            for value in cpu_bursts
        ]

        self.io_bursts = [
            int(value)
            for value in io_bursts
        ]

        self.priority = int(priority)
        self.process_type = str(process_type)

        # ------------------------------------------
        # Validation
        # ------------------------------------------

        if self.arrival_time < 0:
            raise ValueError(
                "arrival_time cannot be negative"
            )

        if not self.cpu_bursts:
            raise ValueError(
                "Process must have at least one CPU burst"
            )

        if any(
            burst <= 0
            for burst in self.cpu_bursts
        ):
            raise ValueError(
                "All CPU bursts must be positive"
            )

        if any(
            burst <= 0
            for burst in self.io_bursts
        ):
            raise ValueError(
                "All I/O bursts must be positive"
            )

        expected_io_count = (
            len(self.cpu_bursts) - 1
        )

        if len(self.io_bursts) != expected_io_count:
            raise ValueError(
                "Number of I/O bursts must equal "
                "number of CPU bursts minus one"
            )

        # Initialize runtime values
        self.reset_runtime()

    # ==================================================
    # Runtime reset
    # ==================================================

    def reset_runtime(self):
        """
        Reset mutable runtime state.

        Useful when running the SAME workload
        with different schedulers.
        """

        self.state = ProcessState.NEW

        self.current_burst_index = 0

        self.remaining_cpu_time = (
            self.cpu_bursts[0]
        )

        # Timing metrics
        self.start_time = None
        self.finish_time = None

        self.response_time = None
        self.turnaround_time = 0
        self.waiting_time = 0

        # Queue/runtime timestamps
        self.ready_since = None
        self.last_run_time = None

        # Runtime statistics
        self.total_cpu_time = 0
        self.total_io_time = 0

        self.times_scheduled = 0
        self.context_switches = 0
        self.preemptions = 0

        # Historical information
        #
        # IMPORTANT:
        # Only completed bursts belong here.
        # These will later become ML features.
        self.cpu_history = []
        self.io_history = []

    # ==================================================
    # Compatibility helpers
    # ==================================================

    @property
    def burst_time(self):
        """
        Compatibility with the Phase 0 schedulers.

        For realistic workloads this represents
        the CURRENT actual CPU burst.

        ML models must NOT receive this value.
        """

        return self.current_cpu_burst

    @property
    def remaining_time(self):
        """
        Compatibility with old Round Robin code.
        """

        return self.remaining_cpu_time

    @remaining_time.setter
    def remaining_time(self, value):
        self.remaining_cpu_time = value

    # ==================================================
    # Current burst information
    # ==================================================

    @property
    def current_cpu_burst(self):
        if self.current_burst_index >= len(
            self.cpu_bursts
        ):
            return 0

        return self.cpu_bursts[
            self.current_burst_index
        ]

    @property
    def current_io_burst(self):
        if self.current_burst_index >= len(
            self.io_bursts
        ):
            return None

        return self.io_bursts[
            self.current_burst_index
        ]

    @property
    def is_finished(self):
        return (
            self.state
            == ProcessState.TERMINATED
        )

    @property
    def cpu_burst_complete(self):
        return self.remaining_cpu_time <= 0

    @property
    def is_last_cpu_burst(self):
        return (
            self.current_burst_index
            == len(self.cpu_bursts) - 1
        )

    # ==================================================
    # State transitions
    # ==================================================

    def mark_ready(self, current_time):
        self.state = ProcessState.READY
        self.ready_since = current_time

    def start_running(self, current_time):
        """
        Process gets the CPU.
        """

        if self.start_time is None:
            self.start_time = current_time

            self.response_time = (
                current_time
                - self.arrival_time
            )

        if self.ready_since is not None:
            self.waiting_time += (
                current_time
                - self.ready_since
            )

        self.state = ProcessState.RUNNING
        self.last_run_time = current_time

        self.times_scheduled += 1

        self.ready_since = None

    def run_for(self, duration):
        """
        Execute the process on CPU for a duration.

        Returns actual executed duration.
        """

        if duration <= 0:
            raise ValueError(
                "duration must be positive"
            )

        actual_duration = min(
            duration,
            self.remaining_cpu_time,
        )

        self.remaining_cpu_time -= (
            actual_duration
        )

        self.total_cpu_time += (
            actual_duration
        )

        return actual_duration

    def preempt(self, current_time):
        """
        CPU is taken from the process before
        its CPU burst finishes.
        """

        if self.cpu_burst_complete:
            raise RuntimeError(
                "Cannot preempt a completed CPU burst"
            )

        self.preemptions += 1

        self.mark_ready(current_time)

    def complete_cpu_burst(self):
        """
        Called after the current CPU burst finishes.

        Returns:
            I/O burst duration if more CPU bursts exist.
            None if this was the final CPU burst.
        """

        if not self.cpu_burst_complete:
            raise RuntimeError(
                "CPU burst has not finished yet"
            )

        completed_burst = self.cpu_bursts[
            self.current_burst_index
        ]

        self.cpu_history.append(
            completed_burst
        )

        if self.is_last_cpu_burst:
            return None

        self.state = ProcessState.BLOCKED

        return self.current_io_burst

    def complete_io(self, current_time):
        """
        Complete current I/O operation and
        prepare the next CPU burst.
        """

        if self.state != ProcessState.BLOCKED:
            raise RuntimeError(
                "Process is not blocked for I/O"
            )

        io_duration = self.io_bursts[
            self.current_burst_index
        ]

        self.io_history.append(
            io_duration
        )

        self.total_io_time += (
            io_duration
        )

        self.current_burst_index += 1

        self.remaining_cpu_time = (
            self.cpu_bursts[
                self.current_burst_index
            ]
        )

        self.mark_ready(current_time)

    def terminate(self, current_time):
        """
        Mark process as finished.
        """

        self.state = ProcessState.TERMINATED

        self.finish_time = current_time

        self.turnaround_time = (
            self.finish_time
            - self.arrival_time
        )

    def record_context_switch(self):
        self.context_switches += 1

    # ==================================================
    # Utilities
    # ==================================================

    def clone(self):
        """
        Create a clean copy of the process.

        Very important for fair scheduler comparisons.
        """

        return Process(
            pid=self.pid,
            arrival_time=self.arrival_time,
            cpu_bursts=self.cpu_bursts.copy(),
            io_bursts=self.io_bursts.copy(),
            priority=self.priority,
            process_type=self.process_type,
        )

    def static_dict(self):
        """
        Static process information.
        """

        return {
            "pid": self.pid,
            "arrival_time": self.arrival_time,
            "priority": self.priority,
            "process_type": self.process_type,
            "cpu_bursts": self.cpu_bursts.copy(),
            "io_bursts": self.io_bursts.copy(),
        }

    def __repr__(self):
        return (
            f"Process("
            f"pid={self.pid}, "
            f"type={self.process_type}, "
            f"arrival={self.arrival_time}, "
            f"priority={self.priority}, "
            f"state={self.state.value}"
            f")"
        )
