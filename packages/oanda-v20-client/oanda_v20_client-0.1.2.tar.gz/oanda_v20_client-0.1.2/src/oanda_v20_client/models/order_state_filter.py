from typing import Literal, Set, cast

OrderStateFilter = Literal["ALL", "CANCELLED", "FILLED", "PENDING", "TRIGGERED"]

ORDER_STATE_FILTER_VALUES: Set[OrderStateFilter] = {
    "ALL",
    "CANCELLED",
    "FILLED",
    "PENDING",
    "TRIGGERED",
}


def check_order_state_filter(value: str) -> OrderStateFilter:
    if value in ORDER_STATE_FILTER_VALUES:
        return cast(OrderStateFilter, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ORDER_STATE_FILTER_VALUES!r}"
    )
