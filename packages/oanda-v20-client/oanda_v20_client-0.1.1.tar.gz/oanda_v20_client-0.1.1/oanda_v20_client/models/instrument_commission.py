from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="InstrumentCommission")


@_attrs_define
class InstrumentCommission:
    """An InstrumentCommission represents an instrument-specific commission

    Attributes:
        commission (Union[Unset, str]): The commission amount (in the Account's home currency) charged per unitsTraded
            of the instrument
        units_traded (Union[Unset, str]): The number of units traded that the commission amount is based on.
        minimum_commission (Union[Unset, str]): The minimum commission amount (in the Account's home currency) that is
            charged when an Order is filled for this instrument.
    """

    commission: Union[Unset, str] = UNSET
    units_traded: Union[Unset, str] = UNSET
    minimum_commission: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        commission = self.commission

        units_traded = self.units_traded

        minimum_commission = self.minimum_commission

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if commission is not UNSET:
            field_dict["commission"] = commission
        if units_traded is not UNSET:
            field_dict["unitsTraded"] = units_traded
        if minimum_commission is not UNSET:
            field_dict["minimumCommission"] = minimum_commission

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        commission = d.pop("commission", UNSET)

        units_traded = d.pop("unitsTraded", UNSET)

        minimum_commission = d.pop("minimumCommission", UNSET)

        instrument_commission = cls(
            commission=commission,
            units_traded=units_traded,
            minimum_commission=minimum_commission,
        )

        instrument_commission.additional_properties = d
        return instrument_commission

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
