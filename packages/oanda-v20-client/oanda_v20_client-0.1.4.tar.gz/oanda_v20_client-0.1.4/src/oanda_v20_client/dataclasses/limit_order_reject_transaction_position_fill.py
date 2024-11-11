from __future__ import annotations
from typing import Literal, Set, cast

LimitOrderRejectTransactionPositionFill = Literal[
    "DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"
]
LIMIT_ORDER_REJECT_TRANSACTION_POSITION_FILL_VALUES: Set[
    LimitOrderRejectTransactionPositionFill
] = {"DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"}


def check_limit_order_reject_transaction_position_fill(
    value: str,
) -> LimitOrderRejectTransactionPositionFill:
    if value in LIMIT_ORDER_REJECT_TRANSACTION_POSITION_FILL_VALUES:
        return cast(LimitOrderRejectTransactionPositionFill, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIMIT_ORDER_REJECT_TRANSACTION_POSITION_FILL_VALUES!r}"
    )
