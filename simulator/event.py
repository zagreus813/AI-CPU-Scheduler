from enum import Enum
from dataclasses import dataclass, field
from typing import Any

class EventType(Enum):
    PROCESS_ARRIVAL = 1
    PROCESS_DISPATCH = 2
    QUANTUM_EXPIRE = 3
    CPU_BURST_COMPLETE = 4
    IO_COMPLETE = 5

@dataclass(order=True)
class Event:
    time: int
    event_type: EventType = field(compare=False)
    process: Any = field(compare=False)  # Using Any to avoid circular import with Process
    
    # Optional snapshot of process state for timeline recording
    snapshot: dict = field(default_factory=dict, compare=False)

    def __repr__(self):
        pid = self.process.pid if self.process else "None"
        return f"Event(time={self.time}, type={self.event_type.name}, process={pid})"
