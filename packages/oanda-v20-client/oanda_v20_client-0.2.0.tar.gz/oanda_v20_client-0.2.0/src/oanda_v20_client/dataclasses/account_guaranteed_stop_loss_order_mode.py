from __future__ import annotations
from typing import Literal, Set, cast

AccountGuaranteedStopLossOrderMode = Literal["ALLOWED", "DISABLED", "REQUIRED"]
ACCOUNT_GUARANTEED_STOP_LOSS_ORDER_MODE_VALUES: Set[
    AccountGuaranteedStopLossOrderMode
] = {"ALLOWED", "DISABLED", "REQUIRED"}


def check_account_guaranteed_stop_loss_order_mode(
    value: str,
) -> AccountGuaranteedStopLossOrderMode:
    if value in ACCOUNT_GUARANTEED_STOP_LOSS_ORDER_MODE_VALUES:
        return cast(AccountGuaranteedStopLossOrderMode, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ACCOUNT_GUARANTEED_STOP_LOSS_ORDER_MODE_VALUES!r}"
    )
