from __future__ import annotations
from typing import Literal, Set, cast

MarketOrderTransactionPositionFill = Literal[
    "DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"
]
MARKET_ORDER_TRANSACTION_POSITION_FILL_VALUES: Set[
    MarketOrderTransactionPositionFill
] = {"DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"}


def check_market_order_transaction_position_fill(
    value: str,
) -> MarketOrderTransactionPositionFill:
    if value in MARKET_ORDER_TRANSACTION_POSITION_FILL_VALUES:
        return cast(MarketOrderTransactionPositionFill, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_ORDER_TRANSACTION_POSITION_FILL_VALUES!r}"
    )
