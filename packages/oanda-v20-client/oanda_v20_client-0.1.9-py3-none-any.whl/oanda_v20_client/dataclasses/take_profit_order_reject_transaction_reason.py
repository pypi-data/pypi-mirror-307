from __future__ import annotations
from typing import Literal, Set, cast

TakeProfitOrderRejectTransactionReason = Literal[
    "CLIENT_ORDER", "ON_FILL", "REPLACEMENT"
]
TAKE_PROFIT_ORDER_REJECT_TRANSACTION_REASON_VALUES: Set[
    TakeProfitOrderRejectTransactionReason
] = {"CLIENT_ORDER", "ON_FILL", "REPLACEMENT"}


def check_take_profit_order_reject_transaction_reason(
    value: str,
) -> TakeProfitOrderRejectTransactionReason:
    if value in TAKE_PROFIT_ORDER_REJECT_TRANSACTION_REASON_VALUES:
        return cast(TakeProfitOrderRejectTransactionReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TAKE_PROFIT_ORDER_REJECT_TRANSACTION_REASON_VALUES!r}"
    )
