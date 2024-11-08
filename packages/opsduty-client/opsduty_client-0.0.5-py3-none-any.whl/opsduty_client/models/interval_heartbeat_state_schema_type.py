from enum import Enum


class IntervalHeartbeatStateSchemaType(str, Enum):
    INTERVAL = "interval"

    def __str__(self) -> str:
        return str(self.value)
