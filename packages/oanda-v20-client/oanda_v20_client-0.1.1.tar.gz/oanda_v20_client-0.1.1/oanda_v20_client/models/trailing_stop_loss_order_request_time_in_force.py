from typing import Literal, Set, cast

TrailingStopLossOrderRequestTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]

TRAILING_STOP_LOSS_ORDER_REQUEST_TIME_IN_FORCE_VALUES: Set[
    TrailingStopLossOrderRequestTimeInForce
] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_trailing_stop_loss_order_request_time_in_force(
    value: str,
) -> TrailingStopLossOrderRequestTimeInForce:
    if value in TRAILING_STOP_LOSS_ORDER_REQUEST_TIME_IN_FORCE_VALUES:
        return cast(TrailingStopLossOrderRequestTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRAILING_STOP_LOSS_ORDER_REQUEST_TIME_IN_FORCE_VALUES!r}"
    )
