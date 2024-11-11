from __future__ import annotations
from typing import Literal, Set, cast

ClientPriceStatus = Literal["invalid", "non-tradeable", "tradeable"]
CLIENT_PRICE_STATUS_VALUES: Set[ClientPriceStatus] = {
    "invalid",
    "non-tradeable",
    "tradeable",
}


def check_client_price_status(value: str) -> ClientPriceStatus:
    if value in CLIENT_PRICE_STATUS_VALUES:
        return cast(ClientPriceStatus, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CLIENT_PRICE_STATUS_VALUES!r}"
    )
