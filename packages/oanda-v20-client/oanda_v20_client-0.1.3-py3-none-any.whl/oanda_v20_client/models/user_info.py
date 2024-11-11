from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="UserInfo")


@_attrs_define
class UserInfo:
    """A representation of user information, as provided to the user themself.

    Attributes:
        username (Union[Unset, str]): The user-provided username.
        user_id (Union[Unset, int]): The user's OANDA-assigned user ID.
        country (Union[Unset, str]): The country that the user is based in.
        email_address (Union[Unset, str]): The user's email address.
    """

    username: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    country: Union[Unset, str] = UNSET
    email_address: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        username = self.username

        user_id = self.user_id

        country = self.country

        email_address = self.email_address

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if username is not UNSET:
            field_dict["username"] = username
        if user_id is not UNSET:
            field_dict["userID"] = user_id
        if country is not UNSET:
            field_dict["country"] = country
        if email_address is not UNSET:
            field_dict["emailAddress"] = email_address

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        username = d.pop("username", UNSET)

        user_id = d.pop("userID", UNSET)

        country = d.pop("country", UNSET)

        email_address = d.pop("emailAddress", UNSET)

        user_info = cls(
            username=username,
            user_id=user_id,
            country=country,
            email_address=email_address,
        )

        user_info.additional_properties = d
        return user_info

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
