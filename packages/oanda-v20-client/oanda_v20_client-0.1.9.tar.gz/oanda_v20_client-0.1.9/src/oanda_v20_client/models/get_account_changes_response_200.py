from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.account_changes import AccountChanges
    from ..models.account_changes_state import AccountChangesState


T = TypeVar("T", bound="GetAccountChangesResponse200")


@_attrs_define
class GetAccountChangesResponse200:
    """
    Attributes:
        changes (Union[Unset, AccountChanges]): An AccountChanges Object is used to represent the changes to an
            Account's Orders, Trades and Positions since a specified Account TransactionID in the past.
        state (Union[Unset, AccountChangesState]): An AccountState Object is used to represent an Account's current
            price-dependent state. Price-dependent Account state is dependent on OANDA's current Prices, and includes things
            like unrealized PL, NAV and Trailing Stop Loss Order state.
        last_transaction_id (Union[Unset, str]): The ID of the last Transaction created for the Account.  This
            Transaction ID should be used for future poll requests, as the client has already observed all changes up to and
            including it.
    """

    changes: Union[Unset, "AccountChanges"] = UNSET
    state: Union[Unset, "AccountChangesState"] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        changes: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.changes, Unset):
            changes = self.changes.to_dict()

        state: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.to_dict()

        last_transaction_id = self.last_transaction_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if changes is not UNSET:
            field_dict["changes"] = changes
        if state is not UNSET:
            field_dict["state"] = state
        if last_transaction_id is not UNSET:
            field_dict["lastTransactionID"] = last_transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.account_changes import AccountChanges
        from ..models.account_changes_state import AccountChangesState

        d = src_dict.copy()
        _changes = d.pop("changes", UNSET)
        changes: Union[Unset, AccountChanges]
        if isinstance(_changes, Unset):
            changes = UNSET
        else:
            changes = AccountChanges.from_dict(_changes)

        _state = d.pop("state", UNSET)
        state: Union[Unset, AccountChangesState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = AccountChangesState.from_dict(_state)

        last_transaction_id = d.pop("lastTransactionID", UNSET)

        get_account_changes_response_200 = cls(
            changes=changes,
            state=state,
            last_transaction_id=last_transaction_id,
        )

        get_account_changes_response_200.additional_properties = d
        return get_account_changes_response_200

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
