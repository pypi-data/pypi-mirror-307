from __future__ import annotations
from typing import Literal, Set, cast

GuaranteedStopLossOrderMode = Literal["ALLOWED", "DISABLED", "REQUIRED"]
GUARANTEED_STOP_LOSS_ORDER_MODE_VALUES: Set[GuaranteedStopLossOrderMode] = {
    "ALLOWED",
    "DISABLED",
    "REQUIRED",
}


def check_guaranteed_stop_loss_order_mode(value: str) -> GuaranteedStopLossOrderMode:
    if value in GUARANTEED_STOP_LOSS_ORDER_MODE_VALUES:
        return cast(GuaranteedStopLossOrderMode, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GUARANTEED_STOP_LOSS_ORDER_MODE_VALUES!r}"
    )
