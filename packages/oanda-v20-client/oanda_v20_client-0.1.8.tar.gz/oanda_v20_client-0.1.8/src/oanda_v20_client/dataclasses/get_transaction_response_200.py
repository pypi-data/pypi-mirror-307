from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .transaction import Transaction
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="GetTransactionResponse200")


@dataclasses.dataclass
class GetTransactionResponse200:
    """Attributes:
    transaction (Union[Unset, Transaction]): The base Transaction specification. Specifies properties that are
        common between all Transaction.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    transaction: Optional["Transaction"]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .transaction import Transaction

        d = src_dict.copy()
        _transaction = d.pop("transaction", None)
        transaction: Optional[Transaction]
        if isinstance(_transaction, Unset):
            transaction = None
        else:
            transaction = Transaction.from_dict(_transaction)
        last_transaction_id = d.pop("lastTransactionID", None)
        get_transaction_response_200 = cls(
            transaction=transaction, last_transaction_id=last_transaction_id
        )
        get_transaction_response_200.additional_properties = d
        return get_transaction_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
