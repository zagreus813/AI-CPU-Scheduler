from collections import Counter

from simulator.process import (
    Process,
    ProcessState,
)

from simulator.workload_generator import (
    WorkloadGenerator,
)


def test_legacy_process():
    """
    Ensure Phase 0 code still works.
    """

    process = Process(
        "P_TEST",
        arrival_time=0,
        burst_time=8,
    )

    assert process.burst_time == 8
    assert process.remaining_time == 8

    print(
        "[PASS] Legacy Process compatibility"
    )


def test_realistic_process():
    process = Process(
        pid="P1",
        arrival_time=3,
        cpu_bursts=[
            4,
            8,
            3,
        ],
        io_bursts=[
            20,
            15,
        ],
        priority=2,
        process_type="interactive",
    )

    assert len(process.cpu_bursts) == 3
    assert len(process.io_bursts) == 2

    assert (
        process.state
        == ProcessState.NEW
    )

    assert process.current_cpu_burst == 4
    assert process.current_io_burst == 20

    print(
        "[PASS] Realistic Process model"
    )


def test_clone():
    process = Process(
        pid="P1",
        arrival_time=0,
        cpu_bursts=[5, 7],
        io_bursts=[20],
        priority=3,
        process_type="io_bound",
    )

    clone = process.clone()

    assert clone is not process

    assert (
        clone.cpu_bursts
        == process.cpu_bursts
    )

    assert (
        clone.io_bursts
        == process.io_bursts
    )

    assert clone.pid == process.pid

    print(
        "[PASS] Process cloning"
    )


def test_workload_generator():
    generator = WorkloadGenerator(
        seed=42
    )

    processes = (
        generator.generate_workload(
            number_of_processes=5000,
            arrival_rate=0.30,
            profile="mixed",
        )
    )

    assert len(processes) == 5000

    # Arrival times must be ordered
    arrival_times = [
        p.arrival_time
        for p in processes
    ]

    assert arrival_times == sorted(
        arrival_times
    )

    # PID must be unique
    pids = [
        p.pid
        for p in processes
    ]

    assert len(set(pids)) == len(pids)

    # Validate every process
    for process in processes:

        assert len(
            process.cpu_bursts
        ) >= 1

        assert len(
            process.io_bursts
        ) == (
            len(process.cpu_bursts)
            - 1
        )

        assert all(
            burst > 0
            for burst in process.cpu_bursts
        )

        assert all(
            burst > 0
            for burst in process.io_bursts
        )

    types = Counter(
        p.process_type
        for p in processes
    )

    print(
        "[PASS] Workload generation"
    )

    print()
    print(
        "Generated processes:",
        len(processes)
    )

    print(
        "Last arrival time:",
        processes[-1].arrival_time
    )

    print()

    print("Process type distribution")

    print("-" * 40)

    for process_type, count in (
        types.items()
    ):
        percentage = (
            count
            / len(processes)
            * 100
        )

        print(
            f"{process_type:<20}"
            f"{count:<10}"
            f"{percentage:.2f}%"
        )

    print()

    total_cpu_bursts = sum(
        len(p.cpu_bursts)
        for p in processes
    )

    total_io_bursts = sum(
        len(p.io_bursts)
        for p in processes
    )

    avg_cpu_bursts = (
        total_cpu_bursts
        / len(processes)
    )

    print(
        "Total CPU bursts:",
        total_cpu_bursts
    )

    print(
        "Total I/O bursts:",
        total_io_bursts
    )

    print(
        "Average CPU bursts/process:",
        f"{avg_cpu_bursts:.2f}"
    )

    print()

    print(
        "Potential future ML samples:",
        total_cpu_bursts
    )


def stress_test():
    generator = WorkloadGenerator(
        seed=123
    )

    processes = (
        generator.generate_workload(
            number_of_processes=100_000,
            arrival_rate=0.50,
            profile="mixed",
        )
    )

    total_samples = sum(
        len(p.cpu_bursts)
        for p in processes
    )

    print()
    print("=" * 60)

    print(
        "[PASS] Stress test"
    )

    print(
        "Processes:",
        len(processes)
    )

    print(
        "Potential ML samples:",
        total_samples
    )

def test_reproducibility():
    generator1 = WorkloadGenerator(seed=42)
    generator2 = WorkloadGenerator(seed=42)

    workload1 = generator1.generate_workload(
        number_of_processes=1000,
        arrival_rate=0.30,
        profile="mixed",
    )

    workload2 = generator2.generate_workload(
        number_of_processes=1000,
        arrival_rate=0.30,
        profile="mixed",
    )

    for p1, p2 in zip(workload1, workload2):
        assert p1.pid == p2.pid
        assert p1.arrival_time == p2.arrival_time
        assert p1.process_type == p2.process_type
        assert p1.priority == p2.priority
        assert p1.cpu_bursts == p2.cpu_bursts
        assert p1.io_bursts == p2.io_bursts

    print(
        "[PASS] Seed reproducibility"
    )


def test_all_profiles():
    profiles = [
        "mixed",
        "interactive_heavy",
        "io_heavy",
        "cpu_heavy",
        "batch_heavy",
    ]

    for profile in profiles:
        generator = WorkloadGenerator(
            seed=42
        )

        processes = (
            generator.generate_workload(
                number_of_processes=1000,
                arrival_rate=0.30,
                profile=profile,
            )
        )

        assert len(processes) == 1000

        assert all(
            len(p.io_bursts)
            == len(p.cpu_bursts) - 1
            for p in processes
        )

        print(
            f"[PASS] Profile: {profile}"
        )
def main():
    print()
    print("=" * 60)
    print("PHASE 1 VALIDATION")
    print("=" * 60)
    print()

    test_legacy_process()

    test_realistic_process()

    test_clone()

    test_workload_generator()

    # Uncomment after normal tests pass.
    #
    test_reproducibility()
    test_all_profiles()
    stress_test()

    print()
    print("=" * 60)
    print("PHASE 1 STATUS: PASS")
    print("=" * 60)


if __name__ == "__main__":
    main()
