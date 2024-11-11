from typing import Literal, Set, cast

LimitOrderTriggerCondition = Literal["ASK", "BID", "DEFAULT", "INVERSE", "MID"]

LIMIT_ORDER_TRIGGER_CONDITION_VALUES: Set[LimitOrderTriggerCondition] = {
    "ASK",
    "BID",
    "DEFAULT",
    "INVERSE",
    "MID",
}


def check_limit_order_trigger_condition(value: str) -> LimitOrderTriggerCondition:
    if value in LIMIT_ORDER_TRIGGER_CONDITION_VALUES:
        return cast(LimitOrderTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIMIT_ORDER_TRIGGER_CONDITION_VALUES!r}"
    )
