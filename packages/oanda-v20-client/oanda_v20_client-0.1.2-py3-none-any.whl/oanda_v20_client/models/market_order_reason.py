from typing import Literal, Set, cast

MarketOrderReason = Literal[
    "CLIENT_ORDER",
    "DELAYED_TRADE_CLOSE",
    "MARGIN_CLOSEOUT",
    "POSITION_CLOSEOUT",
    "TRADE_CLOSE",
]

MARKET_ORDER_REASON_VALUES: Set[MarketOrderReason] = {
    "CLIENT_ORDER",
    "DELAYED_TRADE_CLOSE",
    "MARGIN_CLOSEOUT",
    "POSITION_CLOSEOUT",
    "TRADE_CLOSE",
}


def check_market_order_reason(value: str) -> MarketOrderReason:
    if value in MARKET_ORDER_REASON_VALUES:
        return cast(MarketOrderReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_ORDER_REASON_VALUES!r}"
    )
