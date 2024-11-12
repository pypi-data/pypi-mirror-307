from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="Transaction")


@dataclasses.dataclass
class Transaction:
    """The base Transaction specification. Specifies properties that are common between all Transaction.

    Attributes:
        id (Optional[str]): The Transaction's Identifier.
        time (Optional[str]): The date/time when the Transaction was created.
        user_id (Optional[int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Optional[str]): The ID of the Account the Transaction was created for.
        batch_id (Optional[str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Optional[str]): The Request ID of the request which generated the transaction."""

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", None)
        time = d.pop("time", None)
        user_id = d.pop("userID", None)
        account_id = d.pop("accountID", None)
        batch_id = d.pop("batchID", None)
        request_id = d.pop("requestID", None)
        transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
        )
        return transaction

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
