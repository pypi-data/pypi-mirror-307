from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .transfer_funds_transaction_funding_reason import (
    TransferFundsTransactionFundingReason,
)
from .transfer_funds_transaction_funding_reason import (
    check_transfer_funds_transaction_funding_reason,
)
from .transfer_funds_transaction_type import TransferFundsTransactionType
from .transfer_funds_transaction_type import check_transfer_funds_transaction_type
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="TransferFundsTransaction")


@dataclasses.dataclass
class TransferFundsTransaction:
    """A TransferFundsTransaction represents the transfer of funds in/out of an Account.

    Attributes:
        id (Optional[str]): The Transaction's Identifier.
        time (Optional[str]): The date/time when the Transaction was created.
        user_id (Optional[int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Optional[str]): The ID of the Account the Transaction was created for.
        batch_id (Optional[str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Optional[str]): The Request ID of the request which generated the transaction.
        type (Optional[TransferFundsTransactionType]): The Type of the Transaction. Always set to "TRANSFER_FUNDS"
            in a TransferFundsTransaction.
        amount (Optional[str]): The amount to deposit/withdraw from the Account in the Account's home currency. A
            positive value indicates a deposit, a negative value indicates a withdrawal.
        funding_reason (Optional[TransferFundsTransactionFundingReason]): The reason that an Account is being
            funded.
        comment (Optional[str]): An optional comment that may be attached to a fund transfer for audit purposes
        account_balance (Optional[str]): The Account's balance after funds are transferred."""

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

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", None)
        time = d.pop("time", None)
        user_id = d.pop("userID", None)
        account_id = d.pop("accountID", None)
        batch_id = d.pop("batchID", None)
        request_id = d.pop("requestID", None)
        _type = d.pop("type", None)
        type: Optional[TransferFundsTransactionType]
        if _type is None:
            type = None
        else:
            type = check_transfer_funds_transaction_type(_type)
        amount = d.pop("amount", None)
        _funding_reason = d.pop("fundingReason", None)
        funding_reason: Optional[TransferFundsTransactionFundingReason]
        if _funding_reason is None:
            funding_reason = None
        else:
            funding_reason = check_transfer_funds_transaction_funding_reason(
                _funding_reason
            )
        comment = d.pop("comment", None)
        account_balance = d.pop("accountBalance", None)
        transfer_funds_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
            amount=amount,
            funding_reason=funding_reason,
            comment=comment,
            account_balance=account_balance,
        )
        transfer_funds_transaction.additional_properties = d
        return transfer_funds_transaction

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
