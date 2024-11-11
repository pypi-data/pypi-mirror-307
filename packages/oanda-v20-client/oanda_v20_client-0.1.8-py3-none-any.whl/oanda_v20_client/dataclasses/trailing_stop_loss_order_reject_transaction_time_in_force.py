from __future__ import annotations
from typing import Literal, Set, cast

TrailingStopLossOrderRejectTransactionTimeInForce = Literal[
    "FOK", "GFD", "GTC", "GTD", "IOC"
]
TRAILING_STOP_LOSS_ORDER_REJECT_TRANSACTION_TIME_IN_FORCE_VALUES: Set[
    TrailingStopLossOrderRejectTransactionTimeInForce
] = {"FOK", "GFD", "GTC", "GTD", "IOC"}


def check_trailing_stop_loss_order_reject_transaction_time_in_force(
    value: str,
) -> TrailingStopLossOrderRejectTransactionTimeInForce:
    if value in TRAILING_STOP_LOSS_ORDER_REJECT_TRANSACTION_TIME_IN_FORCE_VALUES:
        return cast(TrailingStopLossOrderRejectTransactionTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRAILING_STOP_LOSS_ORDER_REJECT_TRANSACTION_TIME_IN_FORCE_VALUES!r}"
    )
