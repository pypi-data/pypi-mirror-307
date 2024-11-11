from __future__ import annotations
from typing import Literal, Set, cast

TradeSummaryState = Literal["CLOSE_WHEN_TRADEABLE", "CLOSED", "OPEN"]
TRADE_SUMMARY_STATE_VALUES: Set[TradeSummaryState] = {
    "CLOSE_WHEN_TRADEABLE",
    "CLOSED",
    "OPEN",
}


def check_trade_summary_state(value: str) -> TradeSummaryState:
    if value in TRADE_SUMMARY_STATE_VALUES:
        return cast(TradeSummaryState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRADE_SUMMARY_STATE_VALUES!r}"
    )
