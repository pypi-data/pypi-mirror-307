from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="QuoteHomeConversionFactors")


@_attrs_define
class QuoteHomeConversionFactors:
    """QuoteHomeConversionFactors represents the factors that can be used used to convert quantities of a Price's
    Instrument's quote currency into the Account's home currency.

        Attributes:
            positive_units (Union[Unset, str]): The factor used to convert a positive amount of the Price's Instrument's
                quote currency into a positive amount of the Account's home currency.  Conversion is performed by multiplying
                the quote units by the conversion factor.
            negative_units (Union[Unset, str]): The factor used to convert a negative amount of the Price's Instrument's
                quote currency into a negative amount of the Account's home currency.  Conversion is performed by multiplying
                the quote units by the conversion factor.
    """

    positive_units: Union[Unset, str] = UNSET
    negative_units: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        positive_units = self.positive_units

        negative_units = self.negative_units

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if positive_units is not UNSET:
            field_dict["positiveUnits"] = positive_units
        if negative_units is not UNSET:
            field_dict["negativeUnits"] = negative_units

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        positive_units = d.pop("positiveUnits", UNSET)

        negative_units = d.pop("negativeUnits", UNSET)

        quote_home_conversion_factors = cls(
            positive_units=positive_units,
            negative_units=negative_units,
        )

        quote_home_conversion_factors.additional_properties = d
        return quote_home_conversion_factors

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
