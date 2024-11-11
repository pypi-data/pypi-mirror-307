from __future__ import annotations
from typing import Literal, Set, cast

StopOrderRejectTransactionReason = Literal["CLIENT_ORDER", "REPLACEMENT"]
STOP_ORDER_REJECT_TRANSACTION_REASON_VALUES: Set[StopOrderRejectTransactionReason] = {
    "CLIENT_ORDER",
    "REPLACEMENT",
}


def check_stop_order_reject_transaction_reason(
    value: str,
) -> StopOrderRejectTransactionReason:
    if value in STOP_ORDER_REJECT_TRANSACTION_REASON_VALUES:
        return cast(StopOrderRejectTransactionReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_ORDER_REJECT_TRANSACTION_REASON_VALUES!r}"
    )
