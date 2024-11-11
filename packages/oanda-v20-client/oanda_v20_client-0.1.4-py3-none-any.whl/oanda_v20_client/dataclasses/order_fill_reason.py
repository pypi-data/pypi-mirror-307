from __future__ import annotations
from typing import Literal, Set, cast

OrderFillReason = Literal[
    "LIMIT_ORDER",
    "MARKET_IF_TOUCHED_ORDER",
    "MARKET_ORDER",
    "MARKET_ORDER_DELAYED_TRADE_CLOSE",
    "MARKET_ORDER_MARGIN_CLOSEOUT",
    "MARKET_ORDER_POSITION_CLOSEOUT",
    "MARKET_ORDER_TRADE_CLOSE",
    "STOP_LOSS_ORDER",
    "STOP_ORDER",
    "TAKE_PROFIT_ORDER",
    "TRAILING_STOP_LOSS_ORDER",
]
ORDER_FILL_REASON_VALUES: Set[OrderFillReason] = {
    "LIMIT_ORDER",
    "MARKET_IF_TOUCHED_ORDER",
    "MARKET_ORDER",
    "MARKET_ORDER_DELAYED_TRADE_CLOSE",
    "MARKET_ORDER_MARGIN_CLOSEOUT",
    "MARKET_ORDER_POSITION_CLOSEOUT",
    "MARKET_ORDER_TRADE_CLOSE",
    "STOP_LOSS_ORDER",
    "STOP_ORDER",
    "TAKE_PROFIT_ORDER",
    "TRAILING_STOP_LOSS_ORDER",
}


def check_order_fill_reason(value: str) -> OrderFillReason:
    if value in ORDER_FILL_REASON_VALUES:
        return cast(OrderFillReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ORDER_FILL_REASON_VALUES!r}"
    )
