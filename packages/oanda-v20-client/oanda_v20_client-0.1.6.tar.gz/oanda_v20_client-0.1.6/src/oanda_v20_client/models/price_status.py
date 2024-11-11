from typing import Literal, Set, cast

PriceStatus = Literal["invalid", "non-tradeable", "tradeable"]

PRICE_STATUS_VALUES: Set[PriceStatus] = {
    "invalid",
    "non-tradeable",
    "tradeable",
}


def check_price_status(value: str) -> PriceStatus:
    if value in PRICE_STATUS_VALUES:
        return cast(PriceStatus, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PRICE_STATUS_VALUES!r}"
    )
