from typing import Literal, Set, cast

StopOrderTriggerCondition = Literal["ASK", "BID", "DEFAULT", "INVERSE", "MID"]

STOP_ORDER_TRIGGER_CONDITION_VALUES: Set[StopOrderTriggerCondition] = {
    "ASK",
    "BID",
    "DEFAULT",
    "INVERSE",
    "MID",
}


def check_stop_order_trigger_condition(value: str) -> StopOrderTriggerCondition:
    if value in STOP_ORDER_TRIGGER_CONDITION_VALUES:
        return cast(StopOrderTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_ORDER_TRIGGER_CONDITION_VALUES!r}"
    )
