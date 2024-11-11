from __future__ import annotations
from typing import Literal, Set, cast

StopOrderRequestTriggerCondition = Literal["ASK", "BID", "DEFAULT", "INVERSE", "MID"]
STOP_ORDER_REQUEST_TRIGGER_CONDITION_VALUES: Set[StopOrderRequestTriggerCondition] = {
    "ASK",
    "BID",
    "DEFAULT",
    "INVERSE",
    "MID",
}


def check_stop_order_request_trigger_condition(
    value: str,
) -> StopOrderRequestTriggerCondition:
    if value in STOP_ORDER_REQUEST_TRIGGER_CONDITION_VALUES:
        return cast(StopOrderRequestTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_ORDER_REQUEST_TRIGGER_CONDITION_VALUES!r}"
    )
