from __future__ import annotations
from typing import Literal, Set, cast

MarketOrderRequestType = Literal[
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
]
MARKET_ORDER_REQUEST_TYPE_VALUES: Set[MarketOrderRequestType] = {
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
}


def check_market_order_request_type(value: str) -> MarketOrderRequestType:
    if value in MARKET_ORDER_REQUEST_TYPE_VALUES:
        return cast(MarketOrderRequestType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_ORDER_REQUEST_TYPE_VALUES!r}"
    )
