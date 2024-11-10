from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="ConfigureAccountBody")


@_attrs_define
class ConfigureAccountBody:
    """
    Attributes:
        alias (Union[Unset, str]): Client-defined alias (name) for the Account
        margin_rate (Union[Unset, str]): The string representation of a decimal number.
    """

    alias: Union[Unset, str] = UNSET
    margin_rate: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        alias = self.alias

        margin_rate = self.margin_rate

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if alias is not UNSET:
            field_dict["alias"] = alias
        if margin_rate is not UNSET:
            field_dict["marginRate"] = margin_rate

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        alias = d.pop("alias", UNSET)

        margin_rate = d.pop("marginRate", UNSET)

        configure_account_body = cls(
            alias=alias,
            margin_rate=margin_rate,
        )

        configure_account_body.additional_properties = d
        return configure_account_body

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
