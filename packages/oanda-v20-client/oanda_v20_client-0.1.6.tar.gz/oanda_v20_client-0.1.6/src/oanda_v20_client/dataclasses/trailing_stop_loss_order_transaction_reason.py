from __future__ import annotations
from typing import Literal, Set, cast

TrailingStopLossOrderTransactionReason = Literal[
    "CLIENT_ORDER", "ON_FILL", "REPLACEMENT"
]
TRAILING_STOP_LOSS_ORDER_TRANSACTION_REASON_VALUES: Set[
    TrailingStopLossOrderTransactionReason
] = {"CLIENT_ORDER", "ON_FILL", "REPLACEMENT"}


def check_trailing_stop_loss_order_transaction_reason(
    value: str,
) -> TrailingStopLossOrderTransactionReason:
    if value in TRAILING_STOP_LOSS_ORDER_TRANSACTION_REASON_VALUES:
        return cast(TrailingStopLossOrderTransactionReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRAILING_STOP_LOSS_ORDER_TRANSACTION_REASON_VALUES!r}"
    )
