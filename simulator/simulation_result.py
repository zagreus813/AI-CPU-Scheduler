from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class SimulationResult:
    """
    Structured result returned by the OS Simulator.
    """
    processes: List[Any]
    timeline: List[Dict[str, Any]]
    
    total_time: int
    
    cpu_busy_time: int
    cpu_idle_time: int
    
    context_switch_count: int
    context_switch_time: int
