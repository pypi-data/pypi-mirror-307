from __future__ import annotations
from typing import Literal, Set, cast

TakeProfitOrderTriggerCondition = Literal["ASK", "BID", "DEFAULT", "INVERSE", "MID"]
TAKE_PROFIT_ORDER_TRIGGER_CONDITION_VALUES: Set[TakeProfitOrderTriggerCondition] = {
    "ASK",
    "BID",
    "DEFAULT",
    "INVERSE",
    "MID",
}


def check_take_profit_order_trigger_condition(
    value: str,
) -> TakeProfitOrderTriggerCondition:
    if value in TAKE_PROFIT_ORDER_TRIGGER_CONDITION_VALUES:
        return cast(TakeProfitOrderTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TAKE_PROFIT_ORDER_TRIGGER_CONDITION_VALUES!r}"
    )
