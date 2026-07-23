from enum import Enum


class FeedbackType(str, Enum):
    IDLE = "idle"
    SUCCESS = "success"
    NOBEST = "nobest"
    ERROR = "error"