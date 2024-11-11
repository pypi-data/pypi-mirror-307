from __future__ import annotations
from typing import Literal, Set, cast

MarketIfTouchedOrderTransactionPositionFill = Literal[
    "DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"
]
MARKET_IF_TOUCHED_ORDER_TRANSACTION_POSITION_FILL_VALUES: Set[
    MarketIfTouchedOrderTransactionPositionFill
] = {"DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"}


def check_market_if_touched_order_transaction_position_fill(
    value: str,
) -> MarketIfTouchedOrderTransactionPositionFill:
    if value in MARKET_IF_TOUCHED_ORDER_TRANSACTION_POSITION_FILL_VALUES:
        return cast(MarketIfTouchedOrderTransactionPositionFill, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_IF_TOUCHED_ORDER_TRANSACTION_POSITION_FILL_VALUES!r}"
    )
