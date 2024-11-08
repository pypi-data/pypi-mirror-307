from enum import Enum


class CronHeartbeatStateSchemaType(str, Enum):
    CRON = "cron"

    def __str__(self) -> str:
        return str(self.value)
