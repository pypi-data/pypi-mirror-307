from typing import Literal, Set, cast

TradeStateFilter = Literal["ALL", "CLOSE_WHEN_TRADEABLE", "CLOSED", "OPEN"]

TRADE_STATE_FILTER_VALUES: Set[TradeStateFilter] = {
    "ALL",
    "CLOSE_WHEN_TRADEABLE",
    "CLOSED",
    "OPEN",
}


def check_trade_state_filter(value: str) -> TradeStateFilter:
    if value in TRADE_STATE_FILTER_VALUES:
        return cast(TradeStateFilter, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRADE_STATE_FILTER_VALUES!r}"
    )
