from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .transfer_funds_transaction_funding_reason import (
    TransferFundsTransactionFundingReason,
)
from .transfer_funds_transaction_type import TransferFundsTransactionType
from typing import Optional, TypeVar

T = TypeVar("T", bound="TransferFundsTransaction")


@dataclasses.dataclass
class TransferFundsTransaction:
    """A TransferFundsTransaction represents the transfer of funds in/out of an Account.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, TransferFundsTransactionType]): The Type of the Transaction. Always set to "TRANSFER_FUNDS"
            in a TransferFundsTransaction.
        amount (Union[Unset, str]): The amount to deposit/withdraw from the Account in the Account's home currency. A
            positive value indicates a deposit, a negative value indicates a withdrawal.
        funding_reason (Union[Unset, TransferFundsTransactionFundingReason]): The reason that an Account is being
            funded.
        comment (Union[Unset, str]): An optional comment that may be attached to a fund transfer for audit purposes
        account_balance (Union[Unset, str]): The Account's balance after funds are transferred."""

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]
    type: Optional[TransferFundsTransactionType]
    amount: Optional[str]
    funding_reason: Optional[TransferFundsTransactionFundingReason]
    comment: Optional[str]
    account_balance: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TransferFundsTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
