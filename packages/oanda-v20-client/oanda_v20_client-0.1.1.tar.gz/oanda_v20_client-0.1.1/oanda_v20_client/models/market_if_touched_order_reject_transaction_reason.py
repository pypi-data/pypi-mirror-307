from typing import Literal, Set, cast

MarketIfTouchedOrderRejectTransactionReason = Literal["CLIENT_ORDER", "REPLACEMENT"]

MARKET_IF_TOUCHED_ORDER_REJECT_TRANSACTION_REASON_VALUES: Set[
    MarketIfTouchedOrderRejectTransactionReason
] = {
    "CLIENT_ORDER",
    "REPLACEMENT",
}


def check_market_if_touched_order_reject_transaction_reason(
    value: str,
) -> MarketIfTouchedOrderRejectTransactionReason:
    if value in MARKET_IF_TOUCHED_ORDER_REJECT_TRANSACTION_REASON_VALUES:
        return cast(MarketIfTouchedOrderRejectTransactionReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_IF_TOUCHED_ORDER_REJECT_TRANSACTION_REASON_VALUES!r}"
    )
