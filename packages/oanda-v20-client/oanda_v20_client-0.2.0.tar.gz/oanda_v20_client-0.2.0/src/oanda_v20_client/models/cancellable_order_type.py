from typing import Literal, Set, cast

CancellableOrderType = Literal[
    "LIMIT",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
]

CANCELLABLE_ORDER_TYPE_VALUES: Set[CancellableOrderType] = {
    "LIMIT",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
}


def check_cancellable_order_type(value: str) -> CancellableOrderType:
    if value in CANCELLABLE_ORDER_TYPE_VALUES:
        return cast(CancellableOrderType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CANCELLABLE_ORDER_TYPE_VALUES!r}"
    )
