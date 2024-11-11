from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .delayed_trade_closure_transaction_reason import (
    DelayedTradeClosureTransactionReason,
)
from .delayed_trade_closure_transaction_type import DelayedTradeClosureTransactionType
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

T = TypeVar("T", bound="DelayedTradeClosureTransaction")


@dataclasses.dataclass
class DelayedTradeClosureTransaction:
    """A DelayedTradeClosure Transaction is created administratively to indicate open trades that should have been closed
    but weren't because the open trades' instruments were untradeable at the time. Open trades listed in this
    transaction will be closed once their respective instruments become tradeable.

        Attributes:
            id (Union[Unset, str]): The Transaction's Identifier.
            time (Union[Unset, str]): The date/time when the Transaction was created.
            user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
            account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
            batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
                batch are applied to the Account simultaneously.
            request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
            type (Union[Unset, DelayedTradeClosureTransactionType]): The Type of the Transaction. Always set to
                "DELAYED_TRADE_CLOSURE" for an DelayedTradeClosureTransaction.
            reason (Union[Unset, DelayedTradeClosureTransactionReason]): The reason for the delayed trade closure
            trade_i_ds (Union[Unset, str]): List of Trade ID's identifying the open trades that will be closed when their
                respective instruments become tradeable"""

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, DelayedTradeClosureTransactionType] = UNSET
    reason: Union[Unset, DelayedTradeClosureTransactionReason] = UNSET
    trade_i_ds: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DelayedTradeClosureTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
