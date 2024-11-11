from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .trade_client_extensions_modify_reject_transaction import (
    TradeClientExtensionsModifyRejectTransaction,
)
from types import Unset
from typing import List, Optional, Type, TypeVar, cast

T = TypeVar("T", bound="SetTradeClientExtensionsResponse400")


@dataclasses.dataclass
class SetTradeClientExtensionsResponse400:
    """Attributes:
    trade_client_extensions_modify_reject_transaction (Union[Unset, TradeClientExtensionsModifyRejectTransaction]):
        A TradeClientExtensionsModifyRejectTransaction represents the rejection of the modification of a Trade's Client
        Extensions.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account.
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request.
    error_code (Union[Unset, str]): The code of the error that has occurred. This field may not be returned for some
        errors.
    error_message (Union[Unset, str]): The human-readable description of the error that has occurred."""

    trade_client_extensions_modify_reject_transaction: Optional[
        "TradeClientExtensionsModifyRejectTransaction"
    ]
    last_transaction_id: Optional[str]
    related_transaction_i_ds: Optional[List[str]]
    error_code: Optional[str]
    error_message: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .trade_client_extensions_modify_reject_transaction import (
            TradeClientExtensionsModifyRejectTransaction,
        )

        d = src_dict.copy()
        _trade_client_extensions_modify_reject_transaction = d.pop(
            "tradeClientExtensionsModifyRejectTransaction", None
        )
        trade_client_extensions_modify_reject_transaction: Optional[
            TradeClientExtensionsModifyRejectTransaction
        ]
        if isinstance(_trade_client_extensions_modify_reject_transaction, Unset):
            trade_client_extensions_modify_reject_transaction = None
        else:
            trade_client_extensions_modify_reject_transaction = (
                TradeClientExtensionsModifyRejectTransaction.from_dict(
                    _trade_client_extensions_modify_reject_transaction
                )
            )
        last_transaction_id = d.pop("lastTransactionID", None)
        related_transaction_i_ds = cast(List[str], d.pop("relatedTransactionIDs", None))
        error_code = d.pop("errorCode", None)
        error_message = d.pop("errorMessage", None)
        set_trade_client_extensions_response_400 = cls(
            trade_client_extensions_modify_reject_transaction=trade_client_extensions_modify_reject_transaction,
            last_transaction_id=last_transaction_id,
            related_transaction_i_ds=related_transaction_i_ds,
            error_code=error_code,
            error_message=error_message,
        )
        set_trade_client_extensions_response_400.additional_properties = d
        return set_trade_client_extensions_response_400

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
