from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_price import ClientPrice
from .home_conversions import HomeConversions
from typing import List, Optional, Type, TypeVar

T = TypeVar("T", bound="GetPricesResponse200")


@dataclasses.dataclass
class GetPricesResponse200:
    """Attributes:
    prices (Union[Unset, List['ClientPrice']]): The list of Price objects requested.
    home_conversions (Union[Unset, List['HomeConversions']]): The list of home currency conversion factors
        requested. This field will only be present if includeHomeConversions was set to true in the request.
    time (Union[Unset, str]): The DateTime value to use for the "since" parameter in the next poll request."""

    prices: Optional[List["ClientPrice"]]
    home_conversions: Optional[List["HomeConversions"]]
    time: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .client_price import ClientPrice
        from .home_conversions import HomeConversions

        d = src_dict.copy()
        prices = []
        _prices = d.pop("prices", None)
        for prices_item_data in _prices or []:
            prices_item = ClientPrice.from_dict(prices_item_data)
            prices.append(prices_item)
        home_conversions = []
        _home_conversions = d.pop("homeConversions", None)
        for home_conversions_item_data in _home_conversions or []:
            home_conversions_item = HomeConversions.from_dict(
                home_conversions_item_data
            )
            home_conversions.append(home_conversions_item)
        time = d.pop("time", None)
        get_prices_response_200 = cls(
            prices=prices, home_conversions=home_conversions, time=time
        )
        get_prices_response_200.additional_properties = d
        return get_prices_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
