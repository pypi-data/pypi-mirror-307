from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.client_price import ClientPrice
    from ..models.home_conversions import HomeConversions


T = TypeVar("T", bound="GetPricesResponse200")


@_attrs_define
class GetPricesResponse200:
    """
    Attributes:
        prices (Union[Unset, List['ClientPrice']]): The list of Price objects requested.
        home_conversions (Union[Unset, List['HomeConversions']]): The list of home currency conversion factors
            requested. This field will only be present if includeHomeConversions was set to true in the request.
        time (Union[Unset, str]): The DateTime value to use for the "since" parameter in the next poll request.
    """

    prices: Union[Unset, List["ClientPrice"]] = UNSET
    home_conversions: Union[Unset, List["HomeConversions"]] = UNSET
    time: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prices: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.prices, Unset):
            prices = []
            for prices_item_data in self.prices:
                prices_item = prices_item_data.to_dict()
                prices.append(prices_item)

        home_conversions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.home_conversions, Unset):
            home_conversions = []
            for home_conversions_item_data in self.home_conversions:
                home_conversions_item = home_conversions_item_data.to_dict()
                home_conversions.append(home_conversions_item)

        time = self.time

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if prices is not UNSET:
            field_dict["prices"] = prices
        if home_conversions is not UNSET:
            field_dict["homeConversions"] = home_conversions
        if time is not UNSET:
            field_dict["time"] = time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.client_price import ClientPrice
        from ..models.home_conversions import HomeConversions

        d = src_dict.copy()
        prices = []
        _prices = d.pop("prices", UNSET)
        for prices_item_data in _prices or []:
            prices_item = ClientPrice.from_dict(prices_item_data)

            prices.append(prices_item)

        home_conversions = []
        _home_conversions = d.pop("homeConversions", UNSET)
        for home_conversions_item_data in _home_conversions or []:
            home_conversions_item = HomeConversions.from_dict(
                home_conversions_item_data
            )

            home_conversions.append(home_conversions_item)

        time = d.pop("time", UNSET)

        get_prices_response_200 = cls(
            prices=prices,
            home_conversions=home_conversions,
            time=time,
        )

        get_prices_response_200.additional_properties = d
        return get_prices_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
