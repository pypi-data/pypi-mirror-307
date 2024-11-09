from dataclasses import dataclass


@dataclass
class EventStats:
    """Statistics for an event type"""
    successful_events: int = 0
    failed_events: int = 0
    
    @property
    def total_events(self) -> int:
        return self.successful_events + self.failed_events