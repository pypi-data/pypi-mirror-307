from __future__ import annotations
from typing import Literal, Set, cast

StopLossOrderRequestType = Literal[
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
]
STOP_LOSS_ORDER_REQUEST_TYPE_VALUES: Set[StopLossOrderRequestType] = {
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
}


def check_stop_loss_order_request_type(value: str) -> StopLossOrderRequestType:
    if value in STOP_LOSS_ORDER_REQUEST_TYPE_VALUES:
        return cast(StopLossOrderRequestType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_LOSS_ORDER_REQUEST_TYPE_VALUES!r}"
    )
