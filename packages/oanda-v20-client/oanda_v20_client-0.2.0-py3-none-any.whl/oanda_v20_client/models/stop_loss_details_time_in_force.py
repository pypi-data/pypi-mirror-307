from typing import Literal, Set, cast

StopLossDetailsTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]

STOP_LOSS_DETAILS_TIME_IN_FORCE_VALUES: Set[StopLossDetailsTimeInForce] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_stop_loss_details_time_in_force(value: str) -> StopLossDetailsTimeInForce:
    if value in STOP_LOSS_DETAILS_TIME_IN_FORCE_VALUES:
        return cast(StopLossDetailsTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_LOSS_DETAILS_TIME_IN_FORCE_VALUES!r}"
    )
