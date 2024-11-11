from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="UserInfoExternal")


@_attrs_define
class UserInfoExternal:
    """A representation of user information, as available to external (3rd party) clients.

    Attributes:
        user_id (Union[Unset, int]): The user's OANDA-assigned user ID.
        country (Union[Unset, str]): The country that the user is based in.
        fifo (Union[Unset, bool]): Flag indicating if the the user's Accounts adhere to FIFO execution rules.
    """

    user_id: Union[Unset, int] = UNSET
    country: Union[Unset, str] = UNSET
    fifo: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_id = self.user_id

        country = self.country

        fifo = self.fifo

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if user_id is not UNSET:
            field_dict["userID"] = user_id
        if country is not UNSET:
            field_dict["country"] = country
        if fifo is not UNSET:
            field_dict["FIFO"] = fifo

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_id = d.pop("userID", UNSET)

        country = d.pop("country", UNSET)

        fifo = d.pop("FIFO", UNSET)

        user_info_external = cls(
            user_id=user_id,
            country=country,
            fifo=fifo,
        )

        user_info_external.additional_properties = d
        return user_info_external

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
