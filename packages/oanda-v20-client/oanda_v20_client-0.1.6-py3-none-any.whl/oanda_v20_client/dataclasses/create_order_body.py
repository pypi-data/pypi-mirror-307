from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .order_request import OrderRequest
from typing import Optional, TypeVar

T = TypeVar("T", bound="CreateOrderBody")


@dataclasses.dataclass
class CreateOrderBody:
    """Attributes:
    order (Union[Unset, OrderRequest]): The base Order specification used when requesting that an Order be created.
        Each specific Order-type extends this definition."""

    order: Optional["OrderRequest"]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CreateOrderBody":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
