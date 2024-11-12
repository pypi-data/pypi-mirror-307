from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .order_request import OrderRequest
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="CreateOrderBody")


@dataclasses.dataclass
class CreateOrderBody:
    """Attributes:
    order (Optional[OrderRequest]): The base Order specification used when requesting that an Order be created.
        Each specific Order-type extends this definition."""

    order: Optional["OrderRequest"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .order_request import OrderRequest

        d = src_dict.copy()
        _order = d.pop("order", None)
        order: Optional[OrderRequest]
        if _order is None:
            order = None
        else:
            order = OrderRequest.from_dict(_order)
        create_order_body = cls(order=order)
        return create_order_body

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
