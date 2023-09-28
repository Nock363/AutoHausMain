from enum import Enum

class Status(Enum):
    BOOT="boot"
    SETUP="setup"
    READY="ready"
    RUNNING="running"
    BROKEN="broken"
    