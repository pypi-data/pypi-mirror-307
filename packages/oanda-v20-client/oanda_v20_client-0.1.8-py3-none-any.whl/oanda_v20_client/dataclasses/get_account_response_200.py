from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .account import Account
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="GetAccountResponse200")


@dataclasses.dataclass
class GetAccountResponse200:
    """Attributes:
    account (Union[Unset, Account]): The full details of a client's Account. This includes full open Trade, open
        Position and pending Order representation.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account."""

    account: Optional["Account"]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .account import Account

        d = src_dict.copy()
        _account = d.pop("account", None)
        account: Optional[Account]
        if isinstance(_account, Unset):
            account = None
        else:
            account = Account.from_dict(_account)
        last_transaction_id = d.pop("lastTransactionID", None)
        get_account_response_200 = cls(
            account=account, last_transaction_id=last_transaction_id
        )
        get_account_response_200.additional_properties = d
        return get_account_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
