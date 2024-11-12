from __future__ import annotations
from typing import Literal, Set, cast

StopOrderTransactionTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]
STOP_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES: Set[StopOrderTransactionTimeInForce] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_stop_order_transaction_time_in_force(
    value: str,
) -> StopOrderTransactionTimeInForce:
    if value in STOP_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES:
        return cast(StopOrderTransactionTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES!r}"
    )
