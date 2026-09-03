class FeatureExtractor:
    """
    Extracts features from the system and processes
    at the moment of a scheduling decision.
    """

    @staticmethod
    def extract_system_state(simulator):
        if simulator is None:
            return {}

        cpu_util = 0.0
        if simulator.current_time > 0:
            cpu_util = simulator.cpu_busy_time / simulator.current_time

        running_count = 1 if simulator.running_process else 0
        system_load = len(simulator.ready_queue) + running_count + len(simulator.blocked_processes)

        return {
            "timestamp": simulator.current_time,
            "ready_queue_length": len(simulator.ready_queue),
            "number_of_running_processes": running_count,
            "cpu_utilization": round(cpu_util, 4),
            "system_load": system_load
        }

    @staticmethod
    def extract_process_features(process):
        if process is None:
            return {}
            
        return {
            "process_id": process.pid,
            "process_type": process.process_type,
            "priority": process.priority,
            "arrival_time": process.arrival_time,
            "waiting_time": process.waiting_time,
            "previous_cpu_bursts": process.cpu_history.copy(),
            "previous_io_bursts": process.io_history.copy(),
            "remaining_cpu_time": process.remaining_cpu_time,
            "number_of_context_switches": process.context_switches
        }
