from __future__ import annotations
from typing import Literal, Set, cast

AccountFinancingMode = Literal["DAILY", "NO_FINANCING", "SECOND_BY_SECOND"]
ACCOUNT_FINANCING_MODE_VALUES: Set[AccountFinancingMode] = {
    "DAILY",
    "NO_FINANCING",
    "SECOND_BY_SECOND",
}


def check_account_financing_mode(value: str) -> AccountFinancingMode:
    if value in ACCOUNT_FINANCING_MODE_VALUES:
        return cast(AccountFinancingMode, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ACCOUNT_FINANCING_MODE_VALUES!r}"
    )
