from typing import Literal, Set, cast

StopLossOrderTransactionTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]

STOP_LOSS_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES: Set[
    StopLossOrderTransactionTimeInForce
] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_stop_loss_order_transaction_time_in_force(
    value: str,
) -> StopLossOrderTransactionTimeInForce:
    if value in STOP_LOSS_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES:
        return cast(StopLossOrderTransactionTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_LOSS_ORDER_TRANSACTION_TIME_IN_FORCE_VALUES!r}"
    )
