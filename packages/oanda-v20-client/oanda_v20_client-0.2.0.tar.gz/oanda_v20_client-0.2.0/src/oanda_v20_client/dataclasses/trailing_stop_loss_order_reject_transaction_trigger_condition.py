from __future__ import annotations
from typing import Literal, Set, cast

TrailingStopLossOrderRejectTransactionTriggerCondition = Literal[
    "ASK", "BID", "DEFAULT", "INVERSE", "MID"
]
TRAILING_STOP_LOSS_ORDER_REJECT_TRANSACTION_TRIGGER_CONDITION_VALUES: Set[
    TrailingStopLossOrderRejectTransactionTriggerCondition
] = {"ASK", "BID", "DEFAULT", "INVERSE", "MID"}


def check_trailing_stop_loss_order_reject_transaction_trigger_condition(
    value: str,
) -> TrailingStopLossOrderRejectTransactionTriggerCondition:
    if value in TRAILING_STOP_LOSS_ORDER_REJECT_TRANSACTION_TRIGGER_CONDITION_VALUES:
        return cast(TrailingStopLossOrderRejectTransactionTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRAILING_STOP_LOSS_ORDER_REJECT_TRANSACTION_TRIGGER_CONDITION_VALUES!r}"
    )
