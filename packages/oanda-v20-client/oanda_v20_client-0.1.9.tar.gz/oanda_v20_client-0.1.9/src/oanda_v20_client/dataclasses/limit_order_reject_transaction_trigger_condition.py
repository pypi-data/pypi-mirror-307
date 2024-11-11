from __future__ import annotations
from typing import Literal, Set, cast

LimitOrderRejectTransactionTriggerCondition = Literal[
    "ASK", "BID", "DEFAULT", "INVERSE", "MID"
]
LIMIT_ORDER_REJECT_TRANSACTION_TRIGGER_CONDITION_VALUES: Set[
    LimitOrderRejectTransactionTriggerCondition
] = {"ASK", "BID", "DEFAULT", "INVERSE", "MID"}


def check_limit_order_reject_transaction_trigger_condition(
    value: str,
) -> LimitOrderRejectTransactionTriggerCondition:
    if value in LIMIT_ORDER_REJECT_TRANSACTION_TRIGGER_CONDITION_VALUES:
        return cast(LimitOrderRejectTransactionTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIMIT_ORDER_REJECT_TRANSACTION_TRIGGER_CONDITION_VALUES!r}"
    )
