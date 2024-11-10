from typing import Literal, Set, cast

FixedPriceOrderType = Literal[
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
]

FIXED_PRICE_ORDER_TYPE_VALUES: Set[FixedPriceOrderType] = {
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
}


def check_fixed_price_order_type(value: str) -> FixedPriceOrderType:
    if value in FIXED_PRICE_ORDER_TYPE_VALUES:
        return cast(FixedPriceOrderType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {FIXED_PRICE_ORDER_TYPE_VALUES!r}"
    )
