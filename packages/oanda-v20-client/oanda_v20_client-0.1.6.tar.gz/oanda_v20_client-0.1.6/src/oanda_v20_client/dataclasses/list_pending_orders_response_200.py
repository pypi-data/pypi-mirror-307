from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .order import Order
from typing import List, Optional, TypeVar

T = TypeVar("T", bound="ListPendingOrdersResponse200")


@dataclasses.dataclass
class ListPendingOrdersResponse200:
    """Attributes:
    orders (Union[Unset, List['Order']]): The list of pending Order details
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    orders: Optional[List["Order"]]
    last_transaction_id: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ListPendingOrdersResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
