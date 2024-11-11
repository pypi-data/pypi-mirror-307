from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="OrderIdentifier")


@dataclasses.dataclass
class OrderIdentifier:
    """An OrderIdentifier is used to refer to an Order, and contains both the OrderID and the ClientOrderID.

    Attributes:
        order_id (Union[Unset, str]): The OANDA-assigned Order ID
        client_order_id (Union[Unset, str]): The client-provided client Order ID"""

    order_id: Union[Unset, str] = UNSET
    client_order_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OrderIdentifier":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
