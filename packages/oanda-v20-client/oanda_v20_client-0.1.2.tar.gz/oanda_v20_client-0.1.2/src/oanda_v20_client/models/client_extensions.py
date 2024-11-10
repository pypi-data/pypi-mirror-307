from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="ClientExtensions")


@_attrs_define
class ClientExtensions:
    """A ClientExtensions object allows a client to attach a clientID, tag and comment to Orders and Trades in their
    Account.  Do not set, modify, or delete this field if your account is associated with MT4.

        Attributes:
            id (Union[Unset, str]): The Client ID of the Order/Trade
            tag (Union[Unset, str]): A tag associated with the Order/Trade
            comment (Union[Unset, str]): A comment associated with the Order/Trade
    """

    id: Union[Unset, str] = UNSET
    tag: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        tag = self.tag

        comment = self.comment

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if tag is not UNSET:
            field_dict["tag"] = tag
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        tag = d.pop("tag", UNSET)

        comment = d.pop("comment", UNSET)

        client_extensions = cls(
            id=id,
            tag=tag,
            comment=comment,
        )

        client_extensions.additional_properties = d
        return client_extensions

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
