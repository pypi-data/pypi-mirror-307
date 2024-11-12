from __future__ import annotations
from typing import Literal, Set, cast

TakeProfitOrderRequestType = Literal[
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
]
TAKE_PROFIT_ORDER_REQUEST_TYPE_VALUES: Set[TakeProfitOrderRequestType] = {
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
}


def check_take_profit_order_request_type(value: str) -> TakeProfitOrderRequestType:
    if value in TAKE_PROFIT_ORDER_REQUEST_TYPE_VALUES:
        return cast(TakeProfitOrderRequestType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TAKE_PROFIT_ORDER_REQUEST_TYPE_VALUES!r}"
    )
