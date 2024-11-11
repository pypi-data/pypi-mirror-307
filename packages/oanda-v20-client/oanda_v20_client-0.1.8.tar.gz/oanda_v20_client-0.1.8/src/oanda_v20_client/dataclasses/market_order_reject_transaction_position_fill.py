from __future__ import annotations
from typing import Literal, Set, cast

MarketOrderRejectTransactionPositionFill = Literal[
    "DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"
]
MARKET_ORDER_REJECT_TRANSACTION_POSITION_FILL_VALUES: Set[
    MarketOrderRejectTransactionPositionFill
] = {"DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"}


def check_market_order_reject_transaction_position_fill(
    value: str,
) -> MarketOrderRejectTransactionPositionFill:
    if value in MARKET_ORDER_REJECT_TRANSACTION_POSITION_FILL_VALUES:
        return cast(MarketOrderRejectTransactionPositionFill, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_ORDER_REJECT_TRANSACTION_POSITION_FILL_VALUES!r}"
    )
