from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .transaction import Transaction
from typing import List, Optional, TypeVar

T = TypeVar("T", bound="GetTransactionsSinceIdResponse200")


@dataclasses.dataclass
class GetTransactionsSinceIdResponse200:
    """Attributes:
    transactions (Union[Unset, List['Transaction']]): The list of Transactions that satisfy the request.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    transactions: Optional[List["Transaction"]]
    last_transaction_id: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetTransactionsSinceIdResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
