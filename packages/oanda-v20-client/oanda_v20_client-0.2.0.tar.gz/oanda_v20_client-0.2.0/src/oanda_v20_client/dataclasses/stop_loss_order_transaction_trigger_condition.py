from __future__ import annotations
from typing import Literal, Set, cast

StopLossOrderTransactionTriggerCondition = Literal[
    "ASK", "BID", "DEFAULT", "INVERSE", "MID"
]
STOP_LOSS_ORDER_TRANSACTION_TRIGGER_CONDITION_VALUES: Set[
    StopLossOrderTransactionTriggerCondition
] = {"ASK", "BID", "DEFAULT", "INVERSE", "MID"}


def check_stop_loss_order_transaction_trigger_condition(
    value: str,
) -> StopLossOrderTransactionTriggerCondition:
    if value in STOP_LOSS_ORDER_TRANSACTION_TRIGGER_CONDITION_VALUES:
        return cast(StopLossOrderTransactionTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_LOSS_ORDER_TRANSACTION_TRIGGER_CONDITION_VALUES!r}"
    )
