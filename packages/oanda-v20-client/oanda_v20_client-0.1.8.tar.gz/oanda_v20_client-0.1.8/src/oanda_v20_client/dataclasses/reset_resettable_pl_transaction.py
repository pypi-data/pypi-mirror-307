from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .reset_resettable_pl_transaction_type import ResetResettablePLTransactionType
from .reset_resettable_pl_transaction_type import (
    check_reset_resettable_pl_transaction_type,
)
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="ResetResettablePLTransaction")


@dataclasses.dataclass
class ResetResettablePLTransaction:
    """A ResetResettablePLTransaction represents the resetting of the Account's resettable PL counters.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, ResetResettablePLTransactionType]): The Type of the Transaction. Always set to
            "RESET_RESETTABLE_PL" for a ResetResettablePLTransaction."""

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]
    type: Optional[ResetResettablePLTransactionType]

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
        type: Optional[ResetResettablePLTransactionType]
        if _type is None:
            type = None
        else:
            type = check_reset_resettable_pl_transaction_type(_type)
        reset_resettable_pl_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
        )
        reset_resettable_pl_transaction.additional_properties = d
        return reset_resettable_pl_transaction

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
