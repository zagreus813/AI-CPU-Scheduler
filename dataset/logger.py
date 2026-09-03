from schedulers.base import BaseScheduler
from dataset.feature_extractor import FeatureExtractor

class DecisionLogger(BaseScheduler):
    """
    A wrapper around any BaseScheduler that logs features
    and decisions for ML dataset generation.
    """

    def __init__(self, base_scheduler):
        self.base_scheduler = base_scheduler
        self.simulator = None
        self.decisions = []

    def attach_simulator(self, simulator):
        """
        Allows the logger to access system state.
        """
        self.simulator = simulator

    # If the base scheduler has a current_quantum property, we must expose it
    @property
    def current_quantum(self):
        return getattr(self.base_scheduler, 'current_quantum', None)

    def select_process(self, ready_queue, current_time, system_state=None):
        if not ready_queue:
            return None

        # Extract system features
        system_features = FeatureExtractor.extract_system_state(self.simulator)

        # Extract features for all candidates
        candidate_features = {}
        for p in ready_queue:
            candidate_features[p.pid] = FeatureExtractor.extract_process_features(p)

        # Delegate to base scheduler
        selected_process = self.base_scheduler.select_process(ready_queue, current_time, system_state)

        if selected_process:
            available_candidates = [p.pid for p in ready_queue]
            
            # Create a row for each candidate in the ready queue
            for p in ready_queue:
                decision_record = {
                    "timestamp": system_features.get("timestamp", current_time),
                    "process_id": p.pid,
                    "process_type": candidate_features[p.pid]["process_type"],
                    "priority": candidate_features[p.pid]["priority"],
                    "ready_queue_size": system_features.get("ready_queue_length", len(ready_queue)),
                    "cpu_history": candidate_features[p.pid]["previous_cpu_bursts"],
                    "io_history": candidate_features[p.pid]["previous_io_bursts"],
                    "waiting_time": candidate_features[p.pid]["waiting_time"],
                    "remaining_cpu_time": candidate_features[p.pid]["remaining_cpu_time"],
                    "number_of_context_switches": candidate_features[p.pid]["number_of_context_switches"],
                    
                    # System state
                    "number_of_running_processes": system_features.get("number_of_running_processes", 0),
                    "cpu_utilization": system_features.get("cpu_utilization", 0.0),
                    "system_load": system_features.get("system_load", len(ready_queue)),
                    
                    # Decision info
                    "available_candidates": available_candidates,
                    "scheduler_used": self.base_scheduler.__class__.__name__,
                    "selected": 1 if p.pid == selected_process.pid else 0,
                    
                    # Meta info to populate outcome labels later
                    "_process_ref": p
                }
                self.decisions.append(decision_record)

        return selected_process

    def populate_outcomes(self):
        """
        Called after simulation ends to populate outcome labels
        based on the final state of each process.
        """
        for decision in self.decisions:
            p = decision["_process_ref"]
            
            # Populate outcome labels
            decision["actual_waiting_time"] = p.waiting_time
            decision["turnaround_time"] = p.turnaround_time
            decision["response_time"] = p.response_time
            decision["cpu_usage"] = p.total_cpu_time
            decision["completed_successfully"] = 1 if p.is_finished else 0
            
            # Clean up the reference so it can be serialized easily
            del decision["_process_ref"]
