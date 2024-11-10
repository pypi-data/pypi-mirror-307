from typing import Literal, Set, cast

TradeState = Literal["CLOSE_WHEN_TRADEABLE", "CLOSED", "OPEN"]

TRADE_STATE_VALUES: Set[TradeState] = {
    "CLOSE_WHEN_TRADEABLE",
    "CLOSED",
    "OPEN",
}


def check_trade_state(value: str) -> TradeState:
    if value in TRADE_STATE_VALUES:
        return cast(TradeState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRADE_STATE_VALUES!r}"
    )
