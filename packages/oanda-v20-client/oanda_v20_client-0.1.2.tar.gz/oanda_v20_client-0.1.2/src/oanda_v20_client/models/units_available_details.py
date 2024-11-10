from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="UnitsAvailableDetails")


@_attrs_define
class UnitsAvailableDetails:
    """Representation of many units of an Instrument are available to be traded for both long and short Orders.

    Attributes:
        long (Union[Unset, str]): The units available for long Orders.
        short (Union[Unset, str]): The units available for short Orders.
    """

    long: Union[Unset, str] = UNSET
    short: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        long = self.long

        short = self.short

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if long is not UNSET:
            field_dict["long"] = long
        if short is not UNSET:
            field_dict["short"] = short

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        long = d.pop("long", UNSET)

        short = d.pop("short", UNSET)

        units_available_details = cls(
            long=long,
            short=short,
        )

        units_available_details.additional_properties = d
        return units_available_details

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
