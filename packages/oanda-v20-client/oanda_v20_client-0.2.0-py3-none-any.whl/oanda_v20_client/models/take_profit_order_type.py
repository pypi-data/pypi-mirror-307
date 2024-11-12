from typing import Literal, Set, cast

TakeProfitOrderType = Literal[
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
]

TAKE_PROFIT_ORDER_TYPE_VALUES: Set[TakeProfitOrderType] = {
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
}


def check_take_profit_order_type(value: str) -> TakeProfitOrderType:
    if value in TAKE_PROFIT_ORDER_TYPE_VALUES:
        return cast(TakeProfitOrderType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TAKE_PROFIT_ORDER_TYPE_VALUES!r}"
    )
