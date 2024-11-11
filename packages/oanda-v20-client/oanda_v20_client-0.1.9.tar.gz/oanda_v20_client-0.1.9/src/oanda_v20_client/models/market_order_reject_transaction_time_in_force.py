from typing import Literal, Set, cast

MarketOrderRejectTransactionTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]

MARKET_ORDER_REJECT_TRANSACTION_TIME_IN_FORCE_VALUES: Set[
    MarketOrderRejectTransactionTimeInForce
] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_market_order_reject_transaction_time_in_force(
    value: str,
) -> MarketOrderRejectTransactionTimeInForce:
    if value in MARKET_ORDER_REJECT_TRANSACTION_TIME_IN_FORCE_VALUES:
        return cast(MarketOrderRejectTransactionTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MARKET_ORDER_REJECT_TRANSACTION_TIME_IN_FORCE_VALUES!r}"
    )
