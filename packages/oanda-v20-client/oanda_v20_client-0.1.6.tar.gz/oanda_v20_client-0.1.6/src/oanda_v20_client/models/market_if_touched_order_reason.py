from typing import Literal, Set, cast

MarketIfTouchedOrderReason = Literal["CLIENT_ORDER", "REPLACEMENT"]

MARKET_IF_TOUCHED_ORDER_REASON_VALUES: Set[MarketIfTouchedOrderReason] = {
    "CLIENT_ORDER",
    "REPLACEMENT",
}


def check_market_if_touched_order_reason(value: str) -> MarketIfTouchedOrderReason:
    if value in MARKET_IF_TOUCHED_ORDER_REASON_VALUES:
        return cast(MarketIfTouchedOrderReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_IF_TOUCHED_ORDER_REASON_VALUES!r}"
    )
