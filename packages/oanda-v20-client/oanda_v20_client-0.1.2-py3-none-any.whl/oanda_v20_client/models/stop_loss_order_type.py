from typing import Literal, Set, cast

StopLossOrderType = Literal[
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
]

STOP_LOSS_ORDER_TYPE_VALUES: Set[StopLossOrderType] = {
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
}


def check_stop_loss_order_type(value: str) -> StopLossOrderType:
    if value in STOP_LOSS_ORDER_TYPE_VALUES:
        return cast(StopLossOrderType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_LOSS_ORDER_TYPE_VALUES!r}"
    )
