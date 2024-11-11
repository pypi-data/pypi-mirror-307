from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .client_price import ClientPrice
from .home_conversions import HomeConversions
from typing import List, TypeVar, Union

T = TypeVar("T", bound="GetPricesResponse200")


@dataclasses.dataclass
class GetPricesResponse200:
    """Attributes:
    prices (Union[Unset, List['ClientPrice']]): The list of Price objects requested.
    home_conversions (Union[Unset, List['HomeConversions']]): The list of home currency conversion factors
        requested. This field will only be present if includeHomeConversions was set to true in the request.
    time (Union[Unset, str]): The DateTime value to use for the "since" parameter in the next poll request."""

    prices: Union[Unset, List["ClientPrice"]] = UNSET
    home_conversions: Union[Unset, List["HomeConversions"]] = UNSET
    time: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetPricesResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
