from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="MarketOrderPositionCloseout")


@_attrs_define
class MarketOrderPositionCloseout:
    """A MarketOrderPositionCloseout specifies the extensions to a Market Order when it has been created to closeout a
    specific Position.

        Attributes:
            instrument (Union[Unset, str]): The instrument of the Position being closed out.
            units (Union[Unset, str]): Indication of how much of the Position to close. Either "ALL", or a DecimalNumber
                reflection a partial close of the Trade. The DecimalNumber must always be positive, and represent a number that
                doesn't exceed the absolute size of the Position.
    """

    instrument: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        instrument = self.instrument

        units = self.units

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if instrument is not UNSET:
            field_dict["instrument"] = instrument
        if units is not UNSET:
            field_dict["units"] = units

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        instrument = d.pop("instrument", UNSET)

        units = d.pop("units", UNSET)

        market_order_position_closeout = cls(
            instrument=instrument,
            units=units,
        )

        market_order_position_closeout.additional_properties = d
        return market_order_position_closeout

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
