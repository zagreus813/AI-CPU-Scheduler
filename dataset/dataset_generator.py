import csv
import json
import os
from simulator.workload_generator import WorkloadGenerator
from simulator.simulator import Simulator
from dataset.logger import DecisionLogger

class DatasetGenerator:
    """
    Orchestrates the workload generation, simulation,
    and dataset export for ML training.
    """

    def __init__(self, output_dir="dataset"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate(self, scheduler, num_processes=10000, seed=42, profile="mixed"):
        generator = WorkloadGenerator(seed=seed)
        processes = generator.generate_workload(
            number_of_processes=num_processes,
            arrival_rate=0.3,
            profile=profile
        )

        logger = DecisionLogger(scheduler)
        
        simulator = Simulator(processes, logger, context_switch_cost=1)
        logger.attach_simulator(simulator)

        # Run the simulation to completion
        simulator.run()

        # Populate final outcome labels 
        logger.populate_outcomes()

        return logger.decisions

    def export_csv(self, decisions, filename="scheduler_decisions.csv"):
        filepath = os.path.join(self.output_dir, filename)

        if not decisions:
            return filepath

        fieldnames = list(decisions[0].keys())

        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in decisions:
                # Format arrays as JSON strings for clean CSV export
                row_copy = row.copy()
                row_copy["cpu_history"] = json.dumps(row_copy.get("cpu_history", []))
                row_copy["io_history"] = json.dumps(row_copy.get("io_history", []))
                row_copy["available_candidates"] = json.dumps(row_copy.get("available_candidates", []))
                
                writer.writerow(row_copy)

        return filepath

if __name__ == "__main__":
    from schedulers.fcfs import FCFSScheduler
    
    print("Running Dataset Generator...")
    gen = DatasetGenerator()
    decisions = gen.generate(FCFSScheduler(), num_processes=1000)
    
    csv_path = gen.export_csv(decisions)
    print(f"Generated {len(decisions)} decision records.")
    print(f"Exported to: {csv_path}")
