from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="PriceBucket")


@dataclasses.dataclass
class PriceBucket:
    """A Price Bucket represents a price available for an amount of liquidity

    Attributes:
        price (Union[Unset, str]): The Price offered by the PriceBucket
        liquidity (Union[Unset, int]): The amount of liquidity offered by the PriceBucket"""

    price: Optional[str]
    liquidity: Optional[int]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        price = d.pop("price", None)
        liquidity = d.pop("liquidity", None)
        price_bucket = cls(price=price, liquidity=liquidity)
        price_bucket.additional_properties = d
        return price_bucket

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
