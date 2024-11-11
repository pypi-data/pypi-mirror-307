from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .price import Price
from typing import List, TypeVar, Union

T = TypeVar("T", bound="GetPriceRangeResponse200")


@dataclasses.dataclass
class GetPriceRangeResponse200:
    """Attributes:
    prices (Union[Unset, List['Price']]): The list of prices that satisfy the request."""

    prices: Union[Unset, List["Price"]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetPriceRangeResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
