from typing import Literal, Set, cast

OrderType = Literal[
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
]

ORDER_TYPE_VALUES: Set[OrderType] = {
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
}


def check_order_type(value: str) -> OrderType:
    if value in ORDER_TYPE_VALUES:
        return cast(OrderType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ORDER_TYPE_VALUES!r}"
    )
