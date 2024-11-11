from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .order import Order
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="GetOrderResponse200")


@dataclasses.dataclass
class GetOrderResponse200:
    """Attributes:
    order (Union[Unset, Order]): The base Order definition specifies the properties that are common to all Orders.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account"""

    order: Union[Unset, "Order"] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetOrderResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
