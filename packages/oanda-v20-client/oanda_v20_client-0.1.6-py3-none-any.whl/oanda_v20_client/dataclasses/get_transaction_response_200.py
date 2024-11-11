from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .transaction import Transaction
from typing import Optional, TypeVar

T = TypeVar("T", bound="GetTransactionResponse200")


@dataclasses.dataclass
class GetTransactionResponse200:
    """Attributes:
    transaction (Union[Unset, Transaction]): The base Transaction specification. Specifies properties that are
        common between all Transaction.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    transaction: Optional["Transaction"]
    last_transaction_id: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetTransactionResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
