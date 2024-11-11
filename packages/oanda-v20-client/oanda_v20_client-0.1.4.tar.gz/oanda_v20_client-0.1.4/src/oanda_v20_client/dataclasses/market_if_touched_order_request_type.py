from __future__ import annotations
from typing import Literal, Set, cast

MarketIfTouchedOrderRequestType = Literal[
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
]
MARKET_IF_TOUCHED_ORDER_REQUEST_TYPE_VALUES: Set[MarketIfTouchedOrderRequestType] = {
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
}


def check_market_if_touched_order_request_type(
    value: str,
) -> MarketIfTouchedOrderRequestType:
    if value in MARKET_IF_TOUCHED_ORDER_REQUEST_TYPE_VALUES:
        return cast(MarketIfTouchedOrderRequestType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_IF_TOUCHED_ORDER_REQUEST_TYPE_VALUES!r}"
    )
