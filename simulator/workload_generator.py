import numpy as np

from simulator.process import Process


class WorkloadGenerator:
    """
    Generate reproducible synthetic OS workloads.

    Process types:
        - interactive
        - io_bound
        - cpu_bound
        - batch
    """

    PROFILE_MIXES = {
        "mixed": {
            "interactive": 0.30,
            "io_bound": 0.30,
            "cpu_bound": 0.25,
            "batch": 0.15,
        },

        "interactive_heavy": {
            "interactive": 0.60,
            "io_bound": 0.20,
            "cpu_bound": 0.10,
            "batch": 0.10,
        },

        "io_heavy": {
            "interactive": 0.15,
            "io_bound": 0.60,
            "cpu_bound": 0.15,
            "batch": 0.10,
        },

        "cpu_heavy": {
            "interactive": 0.10,
            "io_bound": 0.10,
            "cpu_bound": 0.60,
            "batch": 0.20,
        },

        "batch_heavy": {
            "interactive": 0.10,
            "io_bound": 0.10,
            "cpu_bound": 0.20,
            "batch": 0.60,
        },
    }

    def __init__(self, seed=42):
        self.seed = seed

        self.rng = (
            np.random.default_rng(seed)
        )

    # ==================================================
    # Helpers
    # ==================================================

    def _lognormal_int(
        self,
        mean,
        sigma,
        minimum,
        maximum,
    ):
        value = self.rng.lognormal(
            mean=mean,
            sigma=sigma,
        )

        value = int(round(value))

        return int(
            np.clip(
                value,
                minimum,
                maximum,
            )
        )

    def _generate_burst_list(
        self,
        count,
        mean,
        sigma,
        minimum,
        maximum,
    ):
        return [
            self._lognormal_int(
                mean=mean,
                sigma=sigma,
                minimum=minimum,
                maximum=maximum,
            )
            for _ in range(count)
        ]

    # ==================================================
    # Interactive
    # ==================================================

    def _generate_interactive(self):
        """
        Short CPU bursts,
        relatively long I/O waits.
        """

        burst_count = int(
            self.rng.integers(
                6,
                16,
            )
        )

        cpu_bursts = (
            self._generate_burst_list(
                count=burst_count,
                mean=1.0,
                sigma=0.45,
                minimum=1,
                maximum=10,
            )
        )

        io_bursts = (
            self._generate_burst_list(
                count=burst_count - 1,
                mean=3.1,
                sigma=0.50,
                minimum=5,
                maximum=80,
            )
        )

        priority = int(
            self.rng.integers(
                0,
                4,
            )
        )

        return (
            cpu_bursts,
            io_bursts,
            priority,
        )

    # ==================================================
    # I/O-bound
    # ==================================================

    def _generate_io_bound(self):
        """
        Short CPU bursts,
        long I/O operations.
        """

        burst_count = int(
            self.rng.integers(
                5,
                13,
            )
        )

        cpu_bursts = (
            self._generate_burst_list(
                count=burst_count,
                mean=1.5,
                sigma=0.55,
                minimum=1,
                maximum=15,
            )
        )

        io_bursts = (
            self._generate_burst_list(
                count=burst_count - 1,
                mean=3.5,
                sigma=0.55,
                minimum=8,
                maximum=120,
            )
        )

        priority = int(
            self.rng.integers(
                2,
                7,
            )
        )

        return (
            cpu_bursts,
            io_bursts,
            priority,
        )

    # ==================================================
    # CPU-bound
    # ==================================================

    def _generate_cpu_bound(self):
        """
        Long CPU bursts,
        short I/O operations.
        """

        burst_count = int(
            self.rng.integers(
                3,
                9,
            )
        )

        cpu_bursts = (
            self._generate_burst_list(
                count=burst_count,
                mean=3.4,
                sigma=0.50,
                minimum=8,
                maximum=100,
            )
        )

        io_bursts = (
            self._generate_burst_list(
                count=burst_count - 1,
                mean=1.4,
                sigma=0.45,
                minimum=1,
                maximum=20,
            )
        )

        priority = int(
            self.rng.integers(
                4,
                10,
            )
        )

        return (
            cpu_bursts,
            io_bursts,
            priority,
        )

    # ==================================================
    # Batch
    # ==================================================

    def _generate_batch(self):
        """
        Large CPU bursts and generally
        lower scheduling priority.
        """

        burst_count = int(
            self.rng.integers(
                2,
                7,
            )
        )

        cpu_bursts = (
            self._generate_burst_list(
                count=burst_count,
                mean=3.9,
                sigma=0.60,
                minimum=15,
                maximum=160,
            )
        )

        io_bursts = (
            self._generate_burst_list(
                count=burst_count - 1,
                mean=2.0,
                sigma=0.50,
                minimum=1,
                maximum=30,
            )
        )

        priority = int(
            self.rng.integers(
                6,
                10,
            )
        )

        return (
            cpu_bursts,
            io_bursts,
            priority,
        )

    # ==================================================
    # Process generation
    # ==================================================

    def generate_process(
        self,
        pid,
        arrival_time,
        process_type,
    ):
        if process_type == "interactive":
            data = (
                self._generate_interactive()
            )

        elif process_type == "io_bound":
            data = (
                self._generate_io_bound()
            )

        elif process_type == "cpu_bound":
            data = (
                self._generate_cpu_bound()
            )

        elif process_type == "batch":
            data = (
                self._generate_batch()
            )

        else:
            raise ValueError(
                f"Unknown process type: "
                f"{process_type}"
            )

        (
            cpu_bursts,
            io_bursts,
            priority,
        ) = data

        return Process(
            pid=pid,
            arrival_time=arrival_time,
            cpu_bursts=cpu_bursts,
            io_bursts=io_bursts,
            priority=priority,
            process_type=process_type,
        )

    # ==================================================
    # Full workload
    # ==================================================

    def generate_workload(
        self,
        number_of_processes=1000,
        arrival_rate=0.30,
        profile="mixed",
    ):
        """
        arrival_rate:
            Average process arrivals
            per simulation time unit.

        Higher value:
            heavier system load.
        """

        if number_of_processes <= 0:
            raise ValueError(
                "number_of_processes must be > 0"
            )

        if arrival_rate <= 0:
            raise ValueError(
                "arrival_rate must be > 0"
            )

        if profile not in self.PROFILE_MIXES:
            raise ValueError(
                f"Unknown profile: {profile}"
            )

        mix = self.PROFILE_MIXES[
            profile
        ]

        process_types = list(
            mix.keys()
        )

        probabilities = list(
            mix.values()
        )

        processes = []

        current_arrival = 0.0

        for index in range(
            number_of_processes
        ):
            if index > 0:
                interarrival = (
                    self.rng.exponential(
                        scale=1 / arrival_rate
                    )
                )

                current_arrival += (
                    interarrival
                )

            arrival_time = int(
                round(current_arrival)
            )

            process_type = (
                self.rng.choice(
                    process_types,
                    p=probabilities,
                )
            )

            process = (
                self.generate_process(
                    pid=f"P{index + 1}",
                    arrival_time=arrival_time,
                    process_type=process_type,
                )
            )

            processes.append(
                process
            )

        return processes
