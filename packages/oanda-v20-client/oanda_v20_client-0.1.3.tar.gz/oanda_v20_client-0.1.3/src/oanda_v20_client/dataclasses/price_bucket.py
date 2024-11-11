from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="PriceBucket")


@dataclasses.dataclass
class PriceBucket:
    """A Price Bucket represents a price available for an amount of liquidity

    Attributes:
        price (Union[Unset, str]): The Price offered by the PriceBucket
        liquidity (Union[Unset, int]): The amount of liquidity offered by the PriceBucket"""

    price: Union[Unset, str] = UNSET
    liquidity: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PriceBucket":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
