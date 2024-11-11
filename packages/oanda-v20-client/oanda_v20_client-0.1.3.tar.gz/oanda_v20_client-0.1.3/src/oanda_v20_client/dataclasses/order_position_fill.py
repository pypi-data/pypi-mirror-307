from __future__ import annotations
from typing import Literal, Set, cast

OrderPositionFill = Literal["DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"]
ORDER_POSITION_FILL_VALUES: Set[OrderPositionFill] = {
    "DEFAULT",
    "OPEN_ONLY",
    "REDUCE_FIRST",
    "REDUCE_ONLY",
}


def check_order_position_fill(value: str) -> OrderPositionFill:
    if value in ORDER_POSITION_FILL_VALUES:
        return cast(OrderPositionFill, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ORDER_POSITION_FILL_VALUES!r}"
    )
