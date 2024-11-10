from typing import Literal, Set, cast

MarketIfTouchedOrderTriggerCondition = Literal[
    "ASK", "BID", "DEFAULT", "INVERSE", "MID"
]

MARKET_IF_TOUCHED_ORDER_TRIGGER_CONDITION_VALUES: Set[
    MarketIfTouchedOrderTriggerCondition
] = {
    "ASK",
    "BID",
    "DEFAULT",
    "INVERSE",
    "MID",
}


def check_market_if_touched_order_trigger_condition(
    value: str,
) -> MarketIfTouchedOrderTriggerCondition:
    if value in MARKET_IF_TOUCHED_ORDER_TRIGGER_CONDITION_VALUES:
        return cast(MarketIfTouchedOrderTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_IF_TOUCHED_ORDER_TRIGGER_CONDITION_VALUES!r}"
    )
