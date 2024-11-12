from __future__ import annotations
from typing import Literal, Set, cast

TrailingStopLossOrderState = Literal["CANCELLED", "FILLED", "PENDING", "TRIGGERED"]
TRAILING_STOP_LOSS_ORDER_STATE_VALUES: Set[TrailingStopLossOrderState] = {
    "CANCELLED",
    "FILLED",
    "PENDING",
    "TRIGGERED",
}


def check_trailing_stop_loss_order_state(value: str) -> TrailingStopLossOrderState:
    if value in TRAILING_STOP_LOSS_ORDER_STATE_VALUES:
        return cast(TrailingStopLossOrderState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRAILING_STOP_LOSS_ORDER_STATE_VALUES!r}"
    )
