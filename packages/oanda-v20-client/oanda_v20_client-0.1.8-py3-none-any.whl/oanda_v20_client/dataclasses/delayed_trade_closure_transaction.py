from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .delayed_trade_closure_transaction_reason import (
    DelayedTradeClosureTransactionReason,
)
from .delayed_trade_closure_transaction_reason import (
    check_delayed_trade_closure_transaction_reason,
)
from .delayed_trade_closure_transaction_type import DelayedTradeClosureTransactionType
from .delayed_trade_closure_transaction_type import (
    check_delayed_trade_closure_transaction_type,
)
from types import Unset
from typing import Optional, Type, TypeVar

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

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", None)
        time = d.pop("time", None)
        user_id = d.pop("userID", None)
        account_id = d.pop("accountID", None)
        batch_id = d.pop("batchID", None)
        request_id = d.pop("requestID", None)
        _type = d.pop("type", None)
        type: Optional[DelayedTradeClosureTransactionType]
        if _type is None:
            type = None
        else:
            type = check_delayed_trade_closure_transaction_type(_type)
        _reason = d.pop("reason", None)
        reason: Optional[DelayedTradeClosureTransactionReason]
        if isinstance(_reason, Unset):
            reason = None
        else:
            reason = check_delayed_trade_closure_transaction_reason(_reason)
        trade_i_ds = d.pop("tradeIDs", None)
        delayed_trade_closure_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
            reason=reason,
            trade_i_ds=trade_i_ds,
        )
        delayed_trade_closure_transaction.additional_properties = d
        return delayed_trade_closure_transaction

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
