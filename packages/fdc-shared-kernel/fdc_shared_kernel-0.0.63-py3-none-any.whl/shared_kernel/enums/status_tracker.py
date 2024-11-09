from enum import Enum


class TaskStatus(Enum):
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"