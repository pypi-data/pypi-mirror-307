from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from .account_changes import AccountChanges
from .account_changes_state import AccountChangesState
from typing import TypeVar, Union

T = TypeVar("T", bound="GetAccountChangesResponse200")


@dataclasses.dataclass
class GetAccountChangesResponse200:
    """Attributes:
    changes (Union[Unset, AccountChanges]): An AccountChanges Object is used to represent the changes to an
        Account's Orders, Trades and Positions since a specified Account TransactionID in the past.
    state (Union[Unset, AccountChangesState]): An AccountState Object is used to represent an Account's current
        price-dependent state. Price-dependent Account state is dependent on OANDA's current Prices, and includes things
        like unrealized PL, NAV and Trailing Stop Loss Order state.
    last_transaction_id (Union[Unset, str]): The ID of the last Transaction created for the Account.  This
        Transaction ID should be used for future poll requests, as the client has already observed all changes up to and
        including it."""

    changes: Union[Unset, "AccountChanges"] = UNSET
    state: Union[Unset, "AccountChangesState"] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GetAccountChangesResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
