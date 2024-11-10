from typing import Literal, Set, cast

LimitOrderRejectTransactionReason = Literal["CLIENT_ORDER", "REPLACEMENT"]

LIMIT_ORDER_REJECT_TRANSACTION_REASON_VALUES: Set[LimitOrderRejectTransactionReason] = {
    "CLIENT_ORDER",
    "REPLACEMENT",
}


def check_limit_order_reject_transaction_reason(
    value: str,
) -> LimitOrderRejectTransactionReason:
    if value in LIMIT_ORDER_REJECT_TRANSACTION_REASON_VALUES:
        return cast(LimitOrderRejectTransactionReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIMIT_ORDER_REJECT_TRANSACTION_REASON_VALUES!r}"
    )
