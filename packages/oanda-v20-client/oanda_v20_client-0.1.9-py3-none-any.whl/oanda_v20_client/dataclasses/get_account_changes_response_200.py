from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .account_changes import AccountChanges
from .account_changes_state import AccountChangesState
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="GetAccountChangesResponse200")


@dataclasses.dataclass
class GetAccountChangesResponse200:
    """Attributes:
    changes (Optional[AccountChanges]): An AccountChanges Object is used to represent the changes to an
        Account's Orders, Trades and Positions since a specified Account TransactionID in the past.
    state (Optional[AccountChangesState]): An AccountState Object is used to represent an Account's current
        price-dependent state. Price-dependent Account state is dependent on OANDA's current Prices, and includes things
        like unrealized PL, NAV and Trailing Stop Loss Order state.
    last_transaction_id (Optional[str]): The ID of the last Transaction created for the Account.  This
        Transaction ID should be used for future poll requests, as the client has already observed all changes up to and
        including it."""

    changes: Optional["AccountChanges"]
    state: Optional["AccountChangesState"]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .account_changes import AccountChanges
        from .account_changes_state import AccountChangesState

        d = src_dict.copy()
        _changes = d.pop("changes", None)
        changes: Optional[AccountChanges]
        if _changes is None:
            changes = None
        else:
            changes = AccountChanges.from_dict(_changes)
        _state = d.pop("state", None)
        state: Optional[AccountChangesState]
        if _state is None:
            state = None
        else:
            state = AccountChangesState.from_dict(_state)
        last_transaction_id = d.pop("lastTransactionID", None)
        get_account_changes_response_200 = cls(
            changes=changes, state=state, last_transaction_id=last_transaction_id
        )
        get_account_changes_response_200.additional_properties = d
        return get_account_changes_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
