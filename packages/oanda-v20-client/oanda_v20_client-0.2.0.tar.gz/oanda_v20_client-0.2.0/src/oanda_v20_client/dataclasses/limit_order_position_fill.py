from __future__ import annotations
from typing import Literal, Set, cast

LimitOrderPositionFill = Literal["DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"]
LIMIT_ORDER_POSITION_FILL_VALUES: Set[LimitOrderPositionFill] = {
    "DEFAULT",
    "OPEN_ONLY",
    "REDUCE_FIRST",
    "REDUCE_ONLY",
}


def check_limit_order_position_fill(value: str) -> LimitOrderPositionFill:
    if value in LIMIT_ORDER_POSITION_FILL_VALUES:
        return cast(LimitOrderPositionFill, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIMIT_ORDER_POSITION_FILL_VALUES!r}"
    )
