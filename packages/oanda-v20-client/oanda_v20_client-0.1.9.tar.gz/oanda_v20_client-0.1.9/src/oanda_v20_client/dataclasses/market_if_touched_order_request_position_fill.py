from __future__ import annotations
from typing import Literal, Set, cast

MarketIfTouchedOrderRequestPositionFill = Literal[
    "DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"
]
MARKET_IF_TOUCHED_ORDER_REQUEST_POSITION_FILL_VALUES: Set[
    MarketIfTouchedOrderRequestPositionFill
] = {"DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"}


def check_market_if_touched_order_request_position_fill(
    value: str,
) -> MarketIfTouchedOrderRequestPositionFill:
    if value in MARKET_IF_TOUCHED_ORDER_REQUEST_POSITION_FILL_VALUES:
        return cast(MarketIfTouchedOrderRequestPositionFill, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_IF_TOUCHED_ORDER_REQUEST_POSITION_FILL_VALUES!r}"
    )
