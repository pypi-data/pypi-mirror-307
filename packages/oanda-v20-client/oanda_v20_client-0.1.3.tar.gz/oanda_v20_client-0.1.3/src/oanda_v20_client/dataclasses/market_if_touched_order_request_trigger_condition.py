from __future__ import annotations
from typing import Literal, Set, cast

MarketIfTouchedOrderRequestTriggerCondition = Literal[
    "ASK", "BID", "DEFAULT", "INVERSE", "MID"
]
MARKET_IF_TOUCHED_ORDER_REQUEST_TRIGGER_CONDITION_VALUES: Set[
    MarketIfTouchedOrderRequestTriggerCondition
] = {"ASK", "BID", "DEFAULT", "INVERSE", "MID"}


def check_market_if_touched_order_request_trigger_condition(
    value: str,
) -> MarketIfTouchedOrderRequestTriggerCondition:
    if value in MARKET_IF_TOUCHED_ORDER_REQUEST_TRIGGER_CONDITION_VALUES:
        return cast(MarketIfTouchedOrderRequestTriggerCondition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_IF_TOUCHED_ORDER_REQUEST_TRIGGER_CONDITION_VALUES!r}"
    )
