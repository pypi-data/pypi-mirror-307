from typing import Literal, Set, cast

StopLossOrderRequestTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]

STOP_LOSS_ORDER_REQUEST_TIME_IN_FORCE_VALUES: Set[StopLossOrderRequestTimeInForce] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_stop_loss_order_request_time_in_force(
    value: str,
) -> StopLossOrderRequestTimeInForce:
    if value in STOP_LOSS_ORDER_REQUEST_TIME_IN_FORCE_VALUES:
        return cast(StopLossOrderRequestTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_LOSS_ORDER_REQUEST_TIME_IN_FORCE_VALUES!r}"
    )
