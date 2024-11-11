from typing import Literal, Set, cast

FixedPriceOrderPositionFill = Literal[
    "DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"
]

FIXED_PRICE_ORDER_POSITION_FILL_VALUES: Set[FixedPriceOrderPositionFill] = {
    "DEFAULT",
    "OPEN_ONLY",
    "REDUCE_FIRST",
    "REDUCE_ONLY",
}


def check_fixed_price_order_position_fill(value: str) -> FixedPriceOrderPositionFill:
    if value in FIXED_PRICE_ORDER_POSITION_FILL_VALUES:
        return cast(FixedPriceOrderPositionFill, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {FIXED_PRICE_ORDER_POSITION_FILL_VALUES!r}"
    )
