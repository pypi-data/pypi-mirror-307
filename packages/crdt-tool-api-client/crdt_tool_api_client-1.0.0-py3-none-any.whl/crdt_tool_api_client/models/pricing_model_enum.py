from enum import Enum


class PricingModelEnum(str, Enum):
    FIXED = "fixed"
    RAMP = "ramp"

    def __str__(self) -> str:
        return str(self.value)
