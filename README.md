# AI CPU Scheduler

An advanced Operating System scheduling simulator combined with a Machine Learning research infrastructure.

The core ambition of this project is to build an **AI-based CPU scheduler**. We are achieving this by first creating a highly realistic OS simulation environment, extracting detailed scheduling datasets, and then using that data to train Machine Learning models capable of making intelligent scheduling decisions.

---

# Project Goal

Traditional CPU schedulers—such as FCFS (First-Come, First-Served), SJF (Shortest Job First), Priority, and Round Robin—rely on static, predefined rules. While effective in predictable environments, they struggle to dynamically adapt to highly volatile, mixed workloads.

This project explores several key research questions:
- Can machine learning accurately predict better scheduling decisions than static algorithms?
- Can an AI-driven scheduler dynamically adapt its strategy to different workloads on the fly?
- Can we effectively optimize for multiple, often conflicting objectives simultaneously, such as:
  - Minimizing Average Waiting Time
  - Minimizing Response Time (Crucial for interactive processes)
  - Minimizing Turnaround Time
  - Maximizing overall CPU Utilization
  - Minimizing Context Switching Overhead

---

# Architecture Overview

The system architecture is designed in modular phases, ensuring strict separation of concerns between the workload generation, the core OS simulation, and the decision-making scheduling policies.

```text
    Workload Generator
           |
           v
     Process Model
           |
           v
 Event-Driven OS Simulator
           |
           v
  Scheduler Interface
           |
  +-----------------+
  |                 |
  v                 v
Traditional      Future AI
Schedulers       Scheduler
  - FCFS          - ML Model
  - SJF Oracle
  - Priority
  - Round Robin
```

---

# Completed Project Phases

## Phase 1 — Process Model and Workload Generation
**Status: ✅ Completed**

Replaced simplistic single-burst models with a highly realistic, stateful OS workload model.

**Features:**
- **Realistic Process Model**: Supports multiple, alternating CPU bursts and I/O wait periods.
- **Process Types**: Capable of generating processes with distinct behavioral profiles, including:
  - `cpu_bound`: Long CPU bursts, minimal I/O.
  - `io_bound`: Short CPU bursts, frequent I/O waits.
  - `interactive`: Highly responsive, lots of short CPU and I/O cycles.
  - `batch`: Low priority, heavy computation processes.
- **Workload Generator**: A fully reproducible, seed-based generator capable of spinning up stress tests of over 100,000+ processes for future ML training dataset generation.

## Phase 2 — Event-Driven OS Simulator
**Status: ✅ Completed**

Developed a robust, highly efficient OS simulation engine.

**Features:**
- **Event-Based Architecture**: Avoids inefficient unit-time stepping by fast-forwarding the global clock to critical events (`PROCESS_ARRIVAL`, `PROCESS_DISPATCH`, `CPU_BURST_COMPLETE`, `IO_COMPLETE`, `QUANTUM_EXPIRE`).
- **Timestamp Event Batching**: All events occurring at the exact same millisecond are processed together before the scheduler is asked to make a new decision.
- **First Dispatch Optimization**: Initial process dispatch does not incur context switch overhead; only active process-to-process preemptions register an overhead cost.
- **Complex OS Mechanics**: Full support for preemption, concurrent I/O blocking, context switch overhead tracking, and precise CPU idle time tracking.

## Phase 3 — Scheduler Architecture
**Status: ✅ Completed**

Completely decoupled the simulation engine from the scheduling decision logic. 

**Features:**
- **Strict Separation of Concerns**: Schedulers are *only* allowed to select the next process. They cannot advance time, execute CPU cycles, handle I/O, or manually modify process states.
- **Baseline Implementations**:
  - `FCFSScheduler`
  - `SJFOracleScheduler` (Uses theoretical knowledge of the next exact burst)
  - `PriorityScheduler`
  - `RoundRobinScheduler`

## Phase 3.5 — Benchmark Framework
**Status: ✅ Completed**

Introduced a benchmarking framework to run identical workloads across multiple schedulers for fair comparison.

**Features:**
- **Metrics Engine**: Calculates average waiting time, turnaround time, response time, CPU utilization, throughput, context switches, and context switch overhead.
- **Export Capabilities**: Automatically saves benchmark reports to both JSON and CSV in the `results/` directory.

### Current Benchmark Results (1,000 Processes, Mixed Profile)
| Scheduler | Waiting Time | Response Time |
|-----------|--------------|---------------|
| **FCFS** | 93344.18 | 10615.88 |
| **SJF Oracle** | 38294.71 | 21672.61 |
| **Priority** | 40113.58 | 32322.00 |
| **Round Robin** | 84238.79 | 1441.39 |

*Observations:* SJF predictably provides the lowest overall waiting time, while Round Robin excels at minimizing response time (at the cost of significantly higher context switching overhead).

## Phase 4 — AI Dataset Generation Pipeline
**Status: ✅ Completed**

Transformed the simulator into a robust data generation pipeline for future Machine Learning models.

**Features:**
- **DecisionLogger Proxy**: Implements a Wrapper pattern around existing traditional schedulers. It seamlessly intercepts the `select_process` call, records the system and candidate features, delegates the decision to the traditional scheduler, and logs the choice.
- **Time-Traveling Outcome Labels**: At the end of the simulation, the logger traverses all generated decision records and pulls the *final* execution metrics (actual waiting time, turnaround time, CPU usage) from the completed Process objects, attaching them as target labels for the ML models.
- **Deep Feature Extraction**: Logs detailed system state (e.g., `cpu_utilization`, `system_load`) and process state (e.g., `cpu_history`, `io_history`, `remaining_cpu_time`) at every single scheduling decision point.
- **Learning-to-Rank Format**: Datasets are exported as CSVs where each row represents a candidate available in the Ready Queue during a scheduling decision, labeled with a binary `selected` target.

---

# Repository Structure

```text
AI-CPU-Scheduler/
├── benchmark/               # Framework for evaluating and exporting scheduler metrics
│   ├── runner.py
│   ├── metrics.py
│   ├── report.py
│   └── export.py
├── dataset/                 # AI Dataset Generation Pipeline (Phase 4)
│   ├── dataset_generator.py # Orchestrates simulation and dataset CSV export
│   ├── feature_extractor.py # Extracts features from processes and system state
│   └── logger.py            # Proxy wrapper for logging scheduler decisions
├── results/                 # Output directory for benchmark JSON/CSV reports
├── schedulers/              # Traditional scheduling algorithms (Phase 3)
│   ├── base.py
│   ├── fcfs.py
│   ├── sjf_oracle.py
│   ├── priority.py
│   └── round_robin.py
├── simulator/               # Core OS Event-Driven Simulation Engine (Phase 1 & 2)
│   ├── event.py
│   ├── process.py
│   ├── simulator.py
│   └── workload_generator.py
└── main.py                  # Entry point for the application
```

---

# Running the Project

**Install Dependencies:**
```bash
python3 -m pip install pytest
```

**Run Tests:**
```bash
python3 -m pytest
```

**Run Benchmark:**
```bash
python3 test_full_benchmark.py
```

**Generate ML Dataset:**
```bash
python3 -m dataset.dataset_generator
```

---

# Future Work

## Phase 5 — Machine Learning Scheduler
With our rich dataset pipeline complete, the next phase focuses entirely on training the ML models.

**Objectives:**
- Train Regression models to predict CPU burst lengths (acting as an AI-driven SJF).
- Train Classification / Learning-to-Rank models to directly select the optimal process from the Ready Queue.
- Evaluate Decision Trees and Neural Networks against the established Phase 3.5 baselines to measure the real-world efficiency of AI-based scheduling.
