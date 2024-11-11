from __future__ import annotations
from typing import Literal, Set, cast

StopOrderTransactionPositionFill = Literal[
    "DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"
]
STOP_ORDER_TRANSACTION_POSITION_FILL_VALUES: Set[StopOrderTransactionPositionFill] = {
    "DEFAULT",
    "OPEN_ONLY",
    "REDUCE_FIRST",
    "REDUCE_ONLY",
}


def check_stop_order_transaction_position_fill(
    value: str,
) -> StopOrderTransactionPositionFill:
    if value in STOP_ORDER_TRANSACTION_POSITION_FILL_VALUES:
        return cast(StopOrderTransactionPositionFill, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_ORDER_TRANSACTION_POSITION_FILL_VALUES!r}"
    )
