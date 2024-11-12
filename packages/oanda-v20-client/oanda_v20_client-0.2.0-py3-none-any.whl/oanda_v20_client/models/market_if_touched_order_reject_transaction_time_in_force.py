from typing import Literal, Set, cast

MarketIfTouchedOrderRejectTransactionTimeInForce = Literal[
    "FOK", "GFD", "GTC", "GTD", "IOC"
]

MARKET_IF_TOUCHED_ORDER_REJECT_TRANSACTION_TIME_IN_FORCE_VALUES: Set[
    MarketIfTouchedOrderRejectTransactionTimeInForce
] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_market_if_touched_order_reject_transaction_time_in_force(
    value: str,
) -> MarketIfTouchedOrderRejectTransactionTimeInForce:
    if value in MARKET_IF_TOUCHED_ORDER_REJECT_TRANSACTION_TIME_IN_FORCE_VALUES:
        return cast(MarketIfTouchedOrderRejectTransactionTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_IF_TOUCHED_ORDER_REJECT_TRANSACTION_TIME_IN_FORCE_VALUES!r}"
    )
