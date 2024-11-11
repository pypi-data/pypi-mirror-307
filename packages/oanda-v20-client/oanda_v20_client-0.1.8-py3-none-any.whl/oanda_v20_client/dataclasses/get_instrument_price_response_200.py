from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .price import Price
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="GetInstrumentPriceResponse200")


@dataclasses.dataclass
class GetInstrumentPriceResponse200:
    """Attributes:
    price (Union[Unset, Price]): The Price representation"""

    price: Optional["Price"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .price import Price

        d = src_dict.copy()
        _price = d.pop("price", None)
        price: Optional[Price]
        if isinstance(_price, Unset):
            price = None
        else:
            price = Price.from_dict(_price)
        get_instrument_price_response_200 = cls(price=price)
        get_instrument_price_response_200.additional_properties = d
        return get_instrument_price_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
