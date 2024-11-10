from typing import Literal, Set, cast

LimitOrderRejectTransactionTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]

LIMIT_ORDER_REJECT_TRANSACTION_TIME_IN_FORCE_VALUES: Set[
    LimitOrderRejectTransactionTimeInForce
] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_limit_order_reject_transaction_time_in_force(
    value: str,
) -> LimitOrderRejectTransactionTimeInForce:
    if value in LIMIT_ORDER_REJECT_TRANSACTION_TIME_IN_FORCE_VALUES:
        return cast(LimitOrderRejectTransactionTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIMIT_ORDER_REJECT_TRANSACTION_TIME_IN_FORCE_VALUES!r}"
    )
