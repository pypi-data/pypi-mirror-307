from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.account_summary import AccountSummary


T = TypeVar("T", bound="GetAccountSummaryResponse200")


@_attrs_define
class GetAccountSummaryResponse200:
    """
    Attributes:
        account (Union[Unset, AccountSummary]): A summary representation of a client's Account. The AccountSummary does
            not provide to full specification of pending Orders, open Trades and Positions.
        last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account.
    """

    account: Union[Unset, "AccountSummary"] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        account: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.account, Unset):
            account = self.account.to_dict()

        last_transaction_id = self.last_transaction_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if account is not UNSET:
            field_dict["account"] = account
        if last_transaction_id is not UNSET:
            field_dict["lastTransactionID"] = last_transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.account_summary import AccountSummary

        d = src_dict.copy()
        _account = d.pop("account", UNSET)
        account: Union[Unset, AccountSummary]
        if isinstance(_account, Unset):
            account = UNSET
        else:
            account = AccountSummary.from_dict(_account)

        last_transaction_id = d.pop("lastTransactionID", UNSET)

        get_account_summary_response_200 = cls(
            account=account,
            last_transaction_id=last_transaction_id,
        )

        get_account_summary_response_200.additional_properties = d
        return get_account_summary_response_200

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
