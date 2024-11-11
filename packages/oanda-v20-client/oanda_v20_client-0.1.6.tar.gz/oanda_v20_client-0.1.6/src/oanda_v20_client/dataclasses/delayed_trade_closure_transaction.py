from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .delayed_trade_closure_transaction_reason import (
    DelayedTradeClosureTransactionReason,
)
from .delayed_trade_closure_transaction_type import DelayedTradeClosureTransactionType
from typing import Optional, TypeVar

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

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]
    type: Optional[DelayedTradeClosureTransactionType]
    reason: Optional[DelayedTradeClosureTransactionReason]
    trade_i_ds: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DelayedTradeClosureTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
