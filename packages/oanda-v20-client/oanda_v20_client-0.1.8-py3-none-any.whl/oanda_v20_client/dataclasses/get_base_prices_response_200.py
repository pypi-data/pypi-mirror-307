from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .price import Price
from typing import List, Optional, Type, TypeVar

T = TypeVar("T", bound="GetBasePricesResponse200")


@dataclasses.dataclass
class GetBasePricesResponse200:
    """Attributes:
    prices (Union[Unset, List['Price']]): The list of prices that satisfy the request."""

    prices: Optional[List["Price"]]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .price import Price

        d = src_dict.copy()
        prices = []
        _prices = d.pop("prices", None)
        for prices_item_data in _prices or []:
            prices_item = Price.from_dict(prices_item_data)
            prices.append(prices_item)
        get_base_prices_response_200 = cls(prices=prices)
        get_base_prices_response_200.additional_properties = d
        return get_base_prices_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
