from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .reset_resettable_pl_transaction_type import ResetResettablePLTransactionType
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

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

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, ResetResettablePLTransactionType] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResetResettablePLTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
