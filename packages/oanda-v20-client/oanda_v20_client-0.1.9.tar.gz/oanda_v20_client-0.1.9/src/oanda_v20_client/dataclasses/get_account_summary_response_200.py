from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .account_summary import AccountSummary
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="GetAccountSummaryResponse200")


@dataclasses.dataclass
class GetAccountSummaryResponse200:
    """Attributes:
    account (Optional[AccountSummary]): A summary representation of a client's Account. The AccountSummary does
        not provide to full specification of pending Orders, open Trades and Positions.
    last_transaction_id (Optional[str]): The ID of the most recent Transaction created for the Account."""

    account: Optional["AccountSummary"]
    last_transaction_id: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .account_summary import AccountSummary

        d = src_dict.copy()
        _account = d.pop("account", None)
        account: Optional[AccountSummary]
        if _account is None:
            account = None
        else:
            account = AccountSummary.from_dict(_account)
        last_transaction_id = d.pop("lastTransactionID", None)
        get_account_summary_response_200 = cls(
            account=account, last_transaction_id=last_transaction_id
        )
        get_account_summary_response_200.additional_properties = d
        return get_account_summary_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
