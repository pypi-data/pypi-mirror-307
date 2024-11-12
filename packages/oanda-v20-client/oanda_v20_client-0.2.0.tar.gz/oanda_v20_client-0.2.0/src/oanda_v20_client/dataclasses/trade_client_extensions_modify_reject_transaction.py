from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from .trade_client_extensions_modify_reject_transaction_reject_reason import (
    TradeClientExtensionsModifyRejectTransactionRejectReason,
)
from .trade_client_extensions_modify_reject_transaction_reject_reason import (
    check_trade_client_extensions_modify_reject_transaction_reject_reason,
)
from .trade_client_extensions_modify_reject_transaction_type import (
    TradeClientExtensionsModifyRejectTransactionType,
)
from .trade_client_extensions_modify_reject_transaction_type import (
    check_trade_client_extensions_modify_reject_transaction_type,
)
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="TradeClientExtensionsModifyRejectTransaction")


@dataclasses.dataclass
class TradeClientExtensionsModifyRejectTransaction:
    """A TradeClientExtensionsModifyRejectTransaction represents the rejection of the modification of a Trade's Client
    Extensions.

        Attributes:
            id (Optional[str]): The Transaction's Identifier.
            time (Optional[str]): The date/time when the Transaction was created.
            user_id (Optional[int]): The ID of the user that initiated the creation of the Transaction.
            account_id (Optional[str]): The ID of the Account the Transaction was created for.
            batch_id (Optional[str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
                batch are applied to the Account simultaneously.
            request_id (Optional[str]): The Request ID of the request which generated the transaction.
            type (Optional[TradeClientExtensionsModifyRejectTransactionType]): The Type of the Transaction. Always set
                to "TRADE_CLIENT_EXTENSIONS_MODIFY_REJECT" for a TradeClientExtensionsModifyRejectTransaction.
            trade_id (Optional[str]): The ID of the Trade who's client extensions are to be modified.
            client_trade_id (Optional[str]): The original Client ID of the Trade who's client extensions are to be
                modified.
            trade_client_extensions_modify (Optional[ClientExtensions]): A ClientExtensions object allows a client to
                attach a clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this
                field if your account is associated with MT4.
            reject_reason (Optional[TradeClientExtensionsModifyRejectTransactionRejectReason]): The reason that the
                Reject Transaction was created"""

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]
    type: Optional[TradeClientExtensionsModifyRejectTransactionType]
    trade_id: Optional[str]
    client_trade_id: Optional[str]
    trade_client_extensions_modify: Optional["ClientExtensions"]
    reject_reason: Optional[TradeClientExtensionsModifyRejectTransactionRejectReason]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .client_extensions import ClientExtensions

        d = src_dict.copy()
        id = d.pop("id", None)
        time = d.pop("time", None)
        user_id = d.pop("userID", None)
        account_id = d.pop("accountID", None)
        batch_id = d.pop("batchID", None)
        request_id = d.pop("requestID", None)
        _type = d.pop("type", None)
        type: Optional[TradeClientExtensionsModifyRejectTransactionType]
        if _type is None:
            type = None
        else:
            type = check_trade_client_extensions_modify_reject_transaction_type(_type)
        trade_id = d.pop("tradeID", None)
        client_trade_id = d.pop("clientTradeID", None)
        _trade_client_extensions_modify = d.pop("tradeClientExtensionsModify", None)
        trade_client_extensions_modify: Optional[ClientExtensions]
        if _trade_client_extensions_modify is None:
            trade_client_extensions_modify = None
        else:
            trade_client_extensions_modify = ClientExtensions.from_dict(
                _trade_client_extensions_modify
            )
        _reject_reason = d.pop("rejectReason", None)
        reject_reason: Optional[
            TradeClientExtensionsModifyRejectTransactionRejectReason
        ]
        if _reject_reason is None:
            reject_reason = None
        else:
            reject_reason = (
                check_trade_client_extensions_modify_reject_transaction_reject_reason(
                    _reject_reason
                )
            )
        trade_client_extensions_modify_reject_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
            trade_id=trade_id,
            client_trade_id=client_trade_id,
            trade_client_extensions_modify=trade_client_extensions_modify,
            reject_reason=reject_reason,
        )
        return trade_client_extensions_modify_reject_transaction

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
