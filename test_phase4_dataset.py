import os
import pytest
import csv
from dataset.dataset_generator import DatasetGenerator
from schedulers.fcfs import FCFSScheduler
from schedulers.sjf_oracle import SJFOracleScheduler

def test_dataset_generation_and_features():
    gen = DatasetGenerator(output_dir="dataset_test")
    decisions = gen.generate(FCFSScheduler(), num_processes=20, seed=42)
    
    assert len(decisions) > 0, "Decision records should be generated"
    
    first = decisions[0]
    expected_keys = [
        "timestamp", "process_id", "process_type", "priority", "ready_queue_size",
        "cpu_history", "io_history", "waiting_time", "remaining_cpu_time", "number_of_context_switches",
        "number_of_running_processes", "cpu_utilization", "system_load",
        "available_candidates", "scheduler_used", "selected",
        "actual_waiting_time", "turnaround_time", "response_time", "cpu_usage", "completed_successfully"
    ]
    
    for key in expected_keys:
        assert key in first, f"Missing feature: {key}"
        
    assert first["scheduler_used"] == "FCFSScheduler"

def test_csv_export(tmp_path):
    gen = DatasetGenerator(output_dir=str(tmp_path))
    decisions = gen.generate(FCFSScheduler(), num_processes=10, seed=42)
    
    csv_path = gen.export_csv(decisions, "test_output.csv")
    
    assert os.path.exists(csv_path), "CSV file should be created"
    assert os.path.getsize(csv_path) > 0, "CSV file should not be empty"
    
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert "process_id" in header
        assert "cpu_history" in header

def test_deterministic_output():
    gen1 = DatasetGenerator(output_dir="dataset_test")
    dec1 = gen1.generate(FCFSScheduler(), num_processes=50, seed=123)
    
    gen2 = DatasetGenerator(output_dir="dataset_test")
    dec2 = gen2.generate(FCFSScheduler(), num_processes=50, seed=123)
    
    assert len(dec1) == len(dec2), "Outputs should have same length"
    
    for r1, r2 in zip(dec1, dec2):
        assert r1["process_id"] == r2["process_id"], "Process IDs must match"
        assert r1["timestamp"] == r2["timestamp"], "Timestamps must match"
        assert r1["selected"] == r2["selected"], "Selections must match"

def test_simulator_compatibility():
    gen = DatasetGenerator(output_dir="dataset_test")
    # SJFOracleScheduler requires remaining_cpu_time access, ensuring wrapping doesn't break it
    decisions = gen.generate(SJFOracleScheduler(), num_processes=20, seed=42)
    
    assert len(decisions) > 0
    # All processes should complete successfully
    for decision in decisions:
        assert decision["completed_successfully"] == 1
