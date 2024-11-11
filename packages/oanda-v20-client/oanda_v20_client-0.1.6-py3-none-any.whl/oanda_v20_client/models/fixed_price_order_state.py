from typing import Literal, Set, cast

FixedPriceOrderState = Literal["CANCELLED", "FILLED", "PENDING", "TRIGGERED"]

FIXED_PRICE_ORDER_STATE_VALUES: Set[FixedPriceOrderState] = {
    "CANCELLED",
    "FILLED",
    "PENDING",
    "TRIGGERED",
}


def check_fixed_price_order_state(value: str) -> FixedPriceOrderState:
    if value in FIXED_PRICE_ORDER_STATE_VALUES:
        return cast(FixedPriceOrderState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {FIXED_PRICE_ORDER_STATE_VALUES!r}"
    )
