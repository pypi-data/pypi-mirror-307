from __future__ import annotations
from typing import Literal, Set, cast

LimitOrderType = Literal[
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
]
LIMIT_ORDER_TYPE_VALUES: Set[LimitOrderType] = {
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
}


def check_limit_order_type(value: str) -> LimitOrderType:
    if value in LIMIT_ORDER_TYPE_VALUES:
        return cast(LimitOrderType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIMIT_ORDER_TYPE_VALUES!r}"
    )
