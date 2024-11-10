from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="HomeConversions")


@_attrs_define
class HomeConversions:
    """HomeConversions represents the factors to use to convert quantities of a given currency into the Account's home
    currency. The conversion factor depends on the scenario the conversion is required for.

        Attributes:
            currency (Union[Unset, str]): The currency to be converted into the home currency.
            account_gain (Union[Unset, str]): The factor used to convert any gains for an Account in the specified currency
                into the Account's home currency. This would include positive realized P/L and positive financing amounts.
                Conversion is performed by multiplying the positive P/L by the conversion factor.
            account_loss (Union[Unset, str]): The string representation of a decimal number.
            position_value (Union[Unset, str]): The factor used to convert a Position or Trade Value in the specified
                currency into the Account's home currency. Conversion is performed by multiplying the Position or Trade Value by
                the conversion factor.
    """

    currency: Union[Unset, str] = UNSET
    account_gain: Union[Unset, str] = UNSET
    account_loss: Union[Unset, str] = UNSET
    position_value: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        currency = self.currency

        account_gain = self.account_gain

        account_loss = self.account_loss

        position_value = self.position_value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if currency is not UNSET:
            field_dict["currency"] = currency
        if account_gain is not UNSET:
            field_dict["accountGain"] = account_gain
        if account_loss is not UNSET:
            field_dict["accountLoss"] = account_loss
        if position_value is not UNSET:
            field_dict["positionValue"] = position_value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        currency = d.pop("currency", UNSET)

        account_gain = d.pop("accountGain", UNSET)

        account_loss = d.pop("accountLoss", UNSET)

        position_value = d.pop("positionValue", UNSET)

        home_conversions = cls(
            currency=currency,
            account_gain=account_gain,
            account_loss=account_loss,
            position_value=position_value,
        )

        home_conversions.additional_properties = d
        return home_conversions

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
