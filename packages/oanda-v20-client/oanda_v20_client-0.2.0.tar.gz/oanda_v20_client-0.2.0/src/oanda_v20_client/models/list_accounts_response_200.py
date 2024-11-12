from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.account_properties import AccountProperties


T = TypeVar("T", bound="ListAccountsResponse200")


@_attrs_define
class ListAccountsResponse200:
    """
    Attributes:
        accounts (Union[Unset, List['AccountProperties']]): The list of Accounts the client is authorized to access and
            their associated properties.
    """

    accounts: Union[Unset, List["AccountProperties"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        accounts: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.accounts, Unset):
            accounts = []
            for accounts_item_data in self.accounts:
                accounts_item = accounts_item_data.to_dict()
                accounts.append(accounts_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if accounts is not UNSET:
            field_dict["accounts"] = accounts

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.account_properties import AccountProperties

        d = src_dict.copy()
        accounts = []
        _accounts = d.pop("accounts", UNSET)
        for accounts_item_data in _accounts or []:
            accounts_item = AccountProperties.from_dict(accounts_item_data)

            accounts.append(accounts_item)

        list_accounts_response_200 = cls(
            accounts=accounts,
        )

        list_accounts_response_200.additional_properties = d
        return list_accounts_response_200

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
