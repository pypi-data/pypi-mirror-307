from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from typing import Optional, TypeVar

T = TypeVar("T", bound="OrderIdentifier")


@dataclasses.dataclass
class OrderIdentifier:
    """An OrderIdentifier is used to refer to an Order, and contains both the OrderID and the ClientOrderID.

    Attributes:
        order_id (Union[Unset, str]): The OANDA-assigned Order ID
        client_order_id (Union[Unset, str]): The client-provided client Order ID"""

    order_id: Optional[str]
    client_order_id: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OrderIdentifier":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
