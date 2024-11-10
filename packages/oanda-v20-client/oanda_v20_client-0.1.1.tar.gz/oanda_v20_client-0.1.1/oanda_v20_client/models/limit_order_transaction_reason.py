from typing import Literal, Set, cast

LimitOrderTransactionReason = Literal["CLIENT_ORDER", "REPLACEMENT"]

LIMIT_ORDER_TRANSACTION_REASON_VALUES: Set[LimitOrderTransactionReason] = {
    "CLIENT_ORDER",
    "REPLACEMENT",
}


def check_limit_order_transaction_reason(value: str) -> LimitOrderTransactionReason:
    if value in LIMIT_ORDER_TRANSACTION_REASON_VALUES:
        return cast(LimitOrderTransactionReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIMIT_ORDER_TRANSACTION_REASON_VALUES!r}"
    )
