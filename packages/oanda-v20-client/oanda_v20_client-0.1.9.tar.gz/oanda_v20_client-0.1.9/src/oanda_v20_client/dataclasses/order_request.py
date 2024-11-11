from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Type, TypeVar

T = TypeVar("T", bound="OrderRequest")


@dataclasses.dataclass
class OrderRequest:
    """The base Order specification used when requesting that an Order be created. Each specific Order-type extends this
    definition."""

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        order_request = cls()
        order_request.additional_properties = d
        return order_request

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
