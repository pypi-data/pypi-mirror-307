from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .transaction import Transaction
from types import UNSET, Unset
from typing import TypeVar
from typing import List
from typing import Union

T = TypeVar("T", bound="GetTransactionsSinceIdResponse200")


@dataclasses.dataclass
class GetTransactionsSinceIdResponse200:
    """Attributes:
    transactions (Union[Unset, List['Transaction']]): The list of Transactions that satisfy the request.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    transactions: Union[Unset, List["Transaction"]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetTransactionsSinceIdResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
