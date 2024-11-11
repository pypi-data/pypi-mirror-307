from __future__ import annotations
from typing import Literal, Set, cast

FundingReason = Literal[
    "ACCOUNT_TRANSFER",
    "ADJUSTMENT",
    "CLIENT_FUNDING",
    "DIVISION_MIGRATION",
    "SITE_MIGRATION",
]
FUNDING_REASON_VALUES: Set[FundingReason] = {
    "ACCOUNT_TRANSFER",
    "ADJUSTMENT",
    "CLIENT_FUNDING",
    "DIVISION_MIGRATION",
    "SITE_MIGRATION",
}


def check_funding_reason(value: str) -> FundingReason:
    if value in FUNDING_REASON_VALUES:
        return cast(FundingReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {FUNDING_REASON_VALUES!r}"
    )
