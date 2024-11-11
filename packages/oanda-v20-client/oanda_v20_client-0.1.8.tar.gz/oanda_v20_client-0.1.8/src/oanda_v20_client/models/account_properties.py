from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union


T = TypeVar("T", bound="AccountProperties")


@_attrs_define
class AccountProperties:
    """Properties related to an Account.

    Attributes:
        id (Union[Unset, str]): The Account's identifier
        mt_4_account_id (Union[Unset, int]): The Account's associated MT4 Account ID. This field will not be present if
            the Account is not an MT4 account.
        tags (Union[Unset, List[str]]): The Account's tags
    """

    id: Union[Unset, str] = UNSET
    mt_4_account_id: Union[Unset, int] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        mt_4_account_id = self.mt_4_account_id

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if mt_4_account_id is not UNSET:
            field_dict["mt4AccountID"] = mt_4_account_id
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        mt_4_account_id = d.pop("mt4AccountID", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        account_properties = cls(
            id=id,
            mt_4_account_id=mt_4_account_id,
            tags=tags,
        )

        account_properties.additional_properties = d
        return account_properties

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
