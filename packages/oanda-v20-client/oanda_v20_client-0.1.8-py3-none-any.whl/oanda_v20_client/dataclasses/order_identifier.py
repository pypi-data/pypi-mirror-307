from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="OrderIdentifier")


@dataclasses.dataclass
class OrderIdentifier:
    """An OrderIdentifier is used to refer to an Order, and contains both the OrderID and the ClientOrderID.

    Attributes:
        order_id (Union[Unset, str]): The OANDA-assigned Order ID
        client_order_id (Union[Unset, str]): The client-provided client Order ID"""

    order_id: Optional[str]
    client_order_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        order_id = d.pop("orderID", None)
        client_order_id = d.pop("clientOrderID", None)
        order_identifier = cls(order_id=order_id, client_order_id=client_order_id)
        order_identifier.additional_properties = d
        return order_identifier

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
