from __future__ import annotations
from typing import Literal, Set, cast

FixedPriceOrderTransactionPositionFill = Literal[
    "DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"
]
FIXED_PRICE_ORDER_TRANSACTION_POSITION_FILL_VALUES: Set[
    FixedPriceOrderTransactionPositionFill
] = {"DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"}


def check_fixed_price_order_transaction_position_fill(
    value: str,
) -> FixedPriceOrderTransactionPositionFill:
    if value in FIXED_PRICE_ORDER_TRANSACTION_POSITION_FILL_VALUES:
        return cast(FixedPriceOrderTransactionPositionFill, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {FIXED_PRICE_ORDER_TRANSACTION_POSITION_FILL_VALUES!r}"
    )
