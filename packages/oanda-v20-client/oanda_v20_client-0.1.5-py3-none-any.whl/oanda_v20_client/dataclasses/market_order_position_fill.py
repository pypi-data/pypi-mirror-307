from __future__ import annotations
from typing import Literal, Set, cast

MarketOrderPositionFill = Literal["DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"]
MARKET_ORDER_POSITION_FILL_VALUES: Set[MarketOrderPositionFill] = {
    "DEFAULT",
    "OPEN_ONLY",
    "REDUCE_FIRST",
    "REDUCE_ONLY",
}


def check_market_order_position_fill(value: str) -> MarketOrderPositionFill:
    if value in MARKET_ORDER_POSITION_FILL_VALUES:
        return cast(MarketOrderPositionFill, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_ORDER_POSITION_FILL_VALUES!r}"
    )
