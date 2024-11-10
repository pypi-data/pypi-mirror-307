from typing import Literal, Set, cast

StopOrderTransactionReason = Literal["CLIENT_ORDER", "REPLACEMENT"]

STOP_ORDER_TRANSACTION_REASON_VALUES: Set[StopOrderTransactionReason] = {
    "CLIENT_ORDER",
    "REPLACEMENT",
}


def check_stop_order_transaction_reason(value: str) -> StopOrderTransactionReason:
    if value in STOP_ORDER_TRANSACTION_REASON_VALUES:
        return cast(StopOrderTransactionReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_ORDER_TRANSACTION_REASON_VALUES!r}"
    )
