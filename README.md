# AI-Based CPU Scheduler

An advanced OS simulator and CPU scheduling project combining traditional Operating Systems principles with Machine Learning.

The ultimate goal of this project is to develop an **AI-Based CPU Scheduler** that predicts the next CPU burst of a process based on historical behavior and system state, using these predictions to make optimal scheduling decisions. Multiple scheduling algorithms will be implemented and compared against this ML-based approach.

## Current Progress

### Phase 0 — Baseline CPU Schedulers
A foundational CPU scheduling simulator was built featuring simple baseline schedulers:
- **FCFS** (First-Come, First-Served)
- **SJF** (Shortest Job First)
- **Round Robin**
These baseline schedulers calculate fundamental metrics such as Waiting Time, Turnaround Time, and Response Time, and produce simple execution timelines.

### Phase 1 — Realistic Process & Workload Model
Replaced the simplistic single-burst process model with a realistic OS workload model. 
- **Process States**: Support for `NEW`, `READY`, `RUNNING`, `BLOCKED`, and `TERMINATED`.
- **Multiple Bursts**: Processes now have alternating CPU and I/O bursts.
- **Process Types**: Supports distinct behaviors including Interactive, I/O-Bound, CPU-Bound, and Batch processing.
- **Workload Generator**: A reproducible, seed-based workload generator capable of simulating massive workloads (e.g., 100,000+ processes) for future ML training dataset generation. 

### Phase 2 — Event-Driven OS Simulator
Developed a highly robust, event-driven OS simulation engine.
- **Event-Based Architecture**: Avoids inefficient unit-time stepping by fast-forwarding to critical events (`PROCESS_ARRIVAL`, `CPU_DISPATCH`, `QUANTUM_EXPIRE`, `IO_COMPLETE`, etc.).
- **Scheduler Decoupling**: Completely separates the simulation engine (`simulator.py`) from scheduling decision logic (`select_process`), allowing for seamless plugging of new schedulers.
- **Complex Features**: Full support for preemption, concurrent I/O blocking, context switch overhead, and precise CPU idle time tracking.
- **Simulation Timeline**: Maintains detailed historical timelines of execution states for precise metric calculations and future ML feature extraction.

## Future Phases
Upcoming phases include integrating classical burst prediction (EMA), developing the Machine Learning models, and finally implementing the AI Scheduler for large-scale experimental comparisons against the baselines.
