from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .price import Price
from typing import Optional, TypeVar

T = TypeVar("T", bound="GetInstrumentPriceResponse200")


@dataclasses.dataclass
class GetInstrumentPriceResponse200:
    """Attributes:
    price (Union[Unset, Price]): The Price representation"""

    price: Optional["Price"]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetInstrumentPriceResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
