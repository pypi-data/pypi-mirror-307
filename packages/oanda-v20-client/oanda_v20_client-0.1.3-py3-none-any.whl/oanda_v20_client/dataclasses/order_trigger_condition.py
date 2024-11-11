from __future__ import annotations
from typing import Literal, Set, cast

OrderTriggerCondition = Literal["ASK", "BID", "DEFAULT", "INVERSE", "MID"]
ORDER_TRIGGER_CONDITION_VALUES: Set[OrderTriggerCondition] = {
    "ASK",
    "BID",
    "DEFAULT",
    "INVERSE",
    "MID",
}


def check_order_trigger_condition(value: str) -> OrderTriggerCondition:
    if value in ORDER_TRIGGER_CONDITION_VALUES:
        return cast(OrderTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ORDER_TRIGGER_CONDITION_VALUES!r}"
    )
