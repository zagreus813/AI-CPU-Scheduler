# AI CPU Scheduler

An Operating System scheduling simulator combined with Machine Learning research infrastructure.

The goal of this project is to build an AI-based CPU scheduler by first creating a realistic OS simulation environment, generating scheduling data, and then training ML models to make scheduling decisions.

---

# Project Goal

Traditional CPU schedulers such as FCFS, SJF, Priority, and Round Robin use predefined rules.

This project explores:

- Can machine learning predict better scheduling decisions?
- Can an AI scheduler adapt to different workloads?
- Can we optimize multiple objectives:
  - Waiting time
  - Response time
  - Turnaround time
  - CPU utilization
  - Context switching overhead

---

# Architecture
Workload Generator
|
v
Process Model
|
v
Event Driven OS Simulator
|
v
Scheduler Interface
|
+----------------+
| |
v v

Traditional Future AI
Schedulers Scheduler

FCFS ML Model
SJF Oracle
Priority
Round Robin


---

# Project Phases

## Phase 1 — Process Model and Workload Generation

Completed.

Implemented:

- Realistic process model
- CPU burst generation
- I/O burst generation
- Process types:
  - CPU bound
  - IO bound
  - Interactive
  - Batch

Validation:


Generated processes: 5000

Total CPU bursts: 38589
Total I/O bursts: 33589

Potential ML samples:
38589


Stress test:


Processes:
100000

Potential ML samples:
766142


Status:

✅ PASS

---

# Phase 2 — Event Driven OS Simulator

Completed.

Implemented:

- Event queue simulation
- Process lifecycle
- CPU execution
- I/O blocking
- Multiple CPU bursts
- Context switch modeling
- CPU idle tracking
- Timeline generation
- Preemption support

Supported events:


PROCESS_ARRIVAL

PROCESS_DISPATCH

CPU_BURST_COMPLETE

IO_COMPLETE

QUANTUM_EXPIRE


Validation:

Tests:


test_phase2_simulator.py

test_phase2_io.py

test_phase2_multi.py

test_phase2_concurrent_io.py

test_phase2_preemption.py


Status:

✅ PASS

---

# Phase 3 — Scheduler Architecture

Completed.

Scheduler abstraction introduced:


BaseScheduler
|
+-- FCFS
|
+-- SJF Oracle
|
+-- Priority
|
+-- Round Robin


Scheduler responsibilities:

Only:


select next process


Scheduler does NOT:

- advance time
- execute CPU
- handle I/O
- modify process state

---

# Phase 3.5 — Benchmark Framework

Completed.

Implemented:

- Benchmark runner
- Scheduler comparison
- Metrics calculation
- JSON export
- CSV export

Metrics:

- Average waiting time
- Average turnaround time
- Average response time
- CPU utilization
- Throughput
- Context switches
- Context switch overhead
- Context switch ratio


---

# Benchmark Result

Configuration:


Processes:
1000

Seed:
42

Profile:
mixed


Results:


Scheduler Waiting Response

FCFS 93344.18 10615.88

SJF 38294.71 21672.61

Priority 40113.58 32322.00

RoundRobin 84238.79 1441.39


Observations:

- SJF provides lowest waiting time.
- Round Robin provides best response time.
- Round Robin has higher context switching overhead.
- Different workloads require different scheduling strategies.

---

# Repository Structure


OSML/

benchmark/
runner.py
metrics.py
report.py
export.py

simulator/
simulator.py
process.py
event.py

schedulers/
base.py
fcfs.py
sjf_oracle.py
priority.py
round_robin.py

results/
benchmark_seed42.json
benchmark_seed42.csv


---

# Running

Install:


python3 -m pip install numpy


Run benchmark:


python3 test_full_benchmark.py


---

# Future Work

## Phase 4

AI Dataset Generation:

Generate scheduling decision data:

Features:

- Ready queue state
- Process history
- CPU bursts
- I/O behavior
- Priority
- Workload characteristics

Labels:

- Best next process

---

## Phase 5

Machine Learning Scheduler:

Models:

- Regression models
- Decision trees
- Neural networks
- Reinforcement learning

Goal:

Replace rule-based scheduling with adaptive AI scheduling.
