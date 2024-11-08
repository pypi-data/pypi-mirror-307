from enum import Enum


class WebhookDeliveryEventStatusEnum(str, Enum):
    FAILED = "failed"
    PENDING = "pending"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
