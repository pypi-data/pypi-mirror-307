from __future__ import annotations
from typing import Literal, Set, cast

TrailingStopLossOrderType = Literal[
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
]
TRAILING_STOP_LOSS_ORDER_TYPE_VALUES: Set[TrailingStopLossOrderType] = {
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
}


def check_trailing_stop_loss_order_type(value: str) -> TrailingStopLossOrderType:
    if value in TRAILING_STOP_LOSS_ORDER_TYPE_VALUES:
        return cast(TrailingStopLossOrderType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRAILING_STOP_LOSS_ORDER_TYPE_VALUES!r}"
    )
