from enum import Enum


class WebhookSubscriptionStatusEnum(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    SUSPENDED = "suspended"

    def __str__(self) -> str:
        return str(self.value)
