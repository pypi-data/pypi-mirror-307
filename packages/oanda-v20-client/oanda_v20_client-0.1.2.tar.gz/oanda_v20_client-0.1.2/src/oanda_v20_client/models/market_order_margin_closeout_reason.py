from typing import Literal, Set, cast

MarketOrderMarginCloseoutReason = Literal[
    "MARGIN_CHECK_VIOLATION",
    "REGULATORY_MARGIN_CALL_VIOLATION",
    "REGULATORY_MARGIN_CHECK_VIOLATION",
]

MARKET_ORDER_MARGIN_CLOSEOUT_REASON_VALUES: Set[MarketOrderMarginCloseoutReason] = {
    "MARGIN_CHECK_VIOLATION",
    "REGULATORY_MARGIN_CALL_VIOLATION",
    "REGULATORY_MARGIN_CHECK_VIOLATION",
}


def check_market_order_margin_closeout_reason(
    value: str,
) -> MarketOrderMarginCloseoutReason:
    if value in MARKET_ORDER_MARGIN_CLOSEOUT_REASON_VALUES:
        return cast(MarketOrderMarginCloseoutReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_ORDER_MARGIN_CLOSEOUT_REASON_VALUES!r}"
    )
