from typing import Literal, Set, cast

StopLossOrderTriggerCondition = Literal["ASK", "BID", "DEFAULT", "INVERSE", "MID"]

STOP_LOSS_ORDER_TRIGGER_CONDITION_VALUES: Set[StopLossOrderTriggerCondition] = {
    "ASK",
    "BID",
    "DEFAULT",
    "INVERSE",
    "MID",
}


def check_stop_loss_order_trigger_condition(
    value: str,
) -> StopLossOrderTriggerCondition:
    if value in STOP_LOSS_ORDER_TRIGGER_CONDITION_VALUES:
        return cast(StopLossOrderTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_LOSS_ORDER_TRIGGER_CONDITION_VALUES!r}"
    )
