from __future__ import annotations
from typing import Literal, Set, cast

StopLossOrderRequestTriggerCondition = Literal[
    "ASK", "BID", "DEFAULT", "INVERSE", "MID"
]
STOP_LOSS_ORDER_REQUEST_TRIGGER_CONDITION_VALUES: Set[
    StopLossOrderRequestTriggerCondition
] = {"ASK", "BID", "DEFAULT", "INVERSE", "MID"}


def check_stop_loss_order_request_trigger_condition(
    value: str,
) -> StopLossOrderRequestTriggerCondition:
    if value in STOP_LOSS_ORDER_REQUEST_TRIGGER_CONDITION_VALUES:
        return cast(StopLossOrderRequestTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_LOSS_ORDER_REQUEST_TRIGGER_CONDITION_VALUES!r}"
    )
