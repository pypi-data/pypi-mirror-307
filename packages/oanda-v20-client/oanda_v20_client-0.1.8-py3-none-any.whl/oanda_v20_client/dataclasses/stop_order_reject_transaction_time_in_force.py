from __future__ import annotations
from typing import Literal, Set, cast

StopOrderRejectTransactionTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]
STOP_ORDER_REJECT_TRANSACTION_TIME_IN_FORCE_VALUES: Set[
    StopOrderRejectTransactionTimeInForce
] = {"FOK", "GFD", "GTC", "GTD", "IOC"}


def check_stop_order_reject_transaction_time_in_force(
    value: str,
) -> StopOrderRejectTransactionTimeInForce:
    if value in STOP_ORDER_REJECT_TRANSACTION_TIME_IN_FORCE_VALUES:
        return cast(StopOrderRejectTransactionTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_ORDER_REJECT_TRANSACTION_TIME_IN_FORCE_VALUES!r}"
    )
