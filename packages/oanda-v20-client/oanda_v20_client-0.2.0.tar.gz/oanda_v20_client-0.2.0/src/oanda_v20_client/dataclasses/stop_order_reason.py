from __future__ import annotations
from typing import Literal, Set, cast

StopOrderReason = Literal["CLIENT_ORDER", "REPLACEMENT"]
STOP_ORDER_REASON_VALUES: Set[StopOrderReason] = {"CLIENT_ORDER", "REPLACEMENT"}


def check_stop_order_reason(value: str) -> StopOrderReason:
    if value in STOP_ORDER_REASON_VALUES:
        return cast(StopOrderReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_ORDER_REASON_VALUES!r}"
    )
