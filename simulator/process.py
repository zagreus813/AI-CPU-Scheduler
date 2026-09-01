class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority

        # Runtime information
        self.remaining_time = burst_time
        self.start_time = None
        self.finish_time = None

        # Performance metrics
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = 0

    def __repr__(self):
        return (
            f"Process("
            f"pid={self.pid}, "
            f"arrival={self.arrival_time}, "
            f"burst={self.burst_time})"
        )
