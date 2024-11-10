from typing import Literal, Set, cast

TransferFundsRejectTransactionFundingReason = Literal[
    "ACCOUNT_TRANSFER",
    "ADJUSTMENT",
    "CLIENT_FUNDING",
    "DIVISION_MIGRATION",
    "SITE_MIGRATION",
]

TRANSFER_FUNDS_REJECT_TRANSACTION_FUNDING_REASON_VALUES: Set[
    TransferFundsRejectTransactionFundingReason
] = {
    "ACCOUNT_TRANSFER",
    "ADJUSTMENT",
    "CLIENT_FUNDING",
    "DIVISION_MIGRATION",
    "SITE_MIGRATION",
}


def check_transfer_funds_reject_transaction_funding_reason(
    value: str,
) -> TransferFundsRejectTransactionFundingReason:
    if value in TRANSFER_FUNDS_REJECT_TRANSACTION_FUNDING_REASON_VALUES:
        return cast(TransferFundsRejectTransactionFundingReason, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRANSFER_FUNDS_REJECT_TRANSACTION_FUNDING_REASON_VALUES!r}"
    )
