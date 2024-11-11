from typing import Literal, Set, cast

StopOrderType = Literal[
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
]

STOP_ORDER_TYPE_VALUES: Set[StopOrderType] = {
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
}


def check_stop_order_type(value: str) -> StopOrderType:
    if value in STOP_ORDER_TYPE_VALUES:
        return cast(StopOrderType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_ORDER_TYPE_VALUES!r}"
    )
