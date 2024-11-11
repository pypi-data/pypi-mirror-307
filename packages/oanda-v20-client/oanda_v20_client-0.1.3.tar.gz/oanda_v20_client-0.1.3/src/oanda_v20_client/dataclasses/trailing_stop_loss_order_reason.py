from __future__ import annotations
from typing import Literal, Set, cast

TrailingStopLossOrderReason = Literal["CLIENT_ORDER", "ON_FILL", "REPLACEMENT"]
TRAILING_STOP_LOSS_ORDER_REASON_VALUES: Set[TrailingStopLossOrderReason] = {
    "CLIENT_ORDER",
    "ON_FILL",
    "REPLACEMENT",
}


def check_trailing_stop_loss_order_reason(value: str) -> TrailingStopLossOrderReason:
    if value in TRAILING_STOP_LOSS_ORDER_REASON_VALUES:
        return cast(TrailingStopLossOrderReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRAILING_STOP_LOSS_ORDER_REASON_VALUES!r}"
    )
