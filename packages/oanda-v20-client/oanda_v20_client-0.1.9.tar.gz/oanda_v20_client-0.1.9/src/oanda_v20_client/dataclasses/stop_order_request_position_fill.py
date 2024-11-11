from __future__ import annotations
from typing import Literal, Set, cast

StopOrderRequestPositionFill = Literal[
    "DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"
]
STOP_ORDER_REQUEST_POSITION_FILL_VALUES: Set[StopOrderRequestPositionFill] = {
    "DEFAULT",
    "OPEN_ONLY",
    "REDUCE_FIRST",
    "REDUCE_ONLY",
}


def check_stop_order_request_position_fill(value: str) -> StopOrderRequestPositionFill:
    if value in STOP_ORDER_REQUEST_POSITION_FILL_VALUES:
        return cast(StopOrderRequestPositionFill, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_ORDER_REQUEST_POSITION_FILL_VALUES!r}"
    )
