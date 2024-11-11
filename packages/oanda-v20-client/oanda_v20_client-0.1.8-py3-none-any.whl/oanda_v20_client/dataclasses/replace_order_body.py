from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .order_request import OrderRequest
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="ReplaceOrderBody")


@dataclasses.dataclass
class ReplaceOrderBody:
    """Attributes:
    order (Union[Unset, OrderRequest]): The base Order specification used when requesting that an Order be created.
        Each specific Order-type extends this definition."""

    order: Optional["OrderRequest"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .order_request import OrderRequest

        d = src_dict.copy()
        _order = d.pop("order", None)
        order: Optional[OrderRequest]
        if isinstance(_order, Unset):
            order = None
        else:
            order = OrderRequest.from_dict(_order)
        replace_order_body = cls(order=order)
        replace_order_body.additional_properties = d
        return replace_order_body

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
