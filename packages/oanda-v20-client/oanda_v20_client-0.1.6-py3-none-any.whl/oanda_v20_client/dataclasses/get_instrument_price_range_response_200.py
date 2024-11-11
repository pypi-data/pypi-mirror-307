from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .price import Price
from typing import List, Optional, TypeVar

T = TypeVar("T", bound="GetInstrumentPriceRangeResponse200")


@dataclasses.dataclass
class GetInstrumentPriceRangeResponse200:
    """Attributes:
    prices (Union[Unset, List['Price']]): The list of prices that satisfy the request."""

    prices: Optional[List["Price"]]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetInstrumentPriceRangeResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
