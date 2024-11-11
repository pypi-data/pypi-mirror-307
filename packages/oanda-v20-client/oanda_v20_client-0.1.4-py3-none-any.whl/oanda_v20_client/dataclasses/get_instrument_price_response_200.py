from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .price import Price
from typing import TypeVar, Union

T = TypeVar("T", bound="GetInstrumentPriceResponse200")


@dataclasses.dataclass
class GetInstrumentPriceResponse200:
    """Attributes:
    price (Union[Unset, Price]): The Price representation"""

    price: Union[Unset, "Price"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetInstrumentPriceResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
