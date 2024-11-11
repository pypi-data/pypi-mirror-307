from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .market_order_reject_transaction import MarketOrderRejectTransaction
from types import Unset
from typing import List, Optional, Type, TypeVar, cast

T = TypeVar("T", bound="CloseTradeResponse404")


@dataclasses.dataclass
class CloseTradeResponse404:
    """Attributes:
    order_reject_transaction (Union[Unset, MarketOrderRejectTransaction]): A MarketOrderRejectTransaction represents
        the rejection of the creation of a Market Order.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account. Only
        present if the Account exists.
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request. Only present if the Account exists.
    error_code (Union[Unset, str]): The code of the error that has occurred. This field may not be returned for some
        errors.
    error_message (Union[Unset, str]): The human-readable description of the error that has occurred."""

    order_reject_transaction: Optional["MarketOrderRejectTransaction"]
    last_transaction_id: Optional[str]
    related_transaction_i_ds: Optional[List[str]]
    error_code: Optional[str]
    error_message: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .market_order_reject_transaction import MarketOrderRejectTransaction

        d = src_dict.copy()
        _order_reject_transaction = d.pop("orderRejectTransaction", None)
        order_reject_transaction: Optional[MarketOrderRejectTransaction]
        if isinstance(_order_reject_transaction, Unset):
            order_reject_transaction = None
        else:
            order_reject_transaction = MarketOrderRejectTransaction.from_dict(
                _order_reject_transaction
            )
        last_transaction_id = d.pop("lastTransactionID", None)
        related_transaction_i_ds = cast(List[str], d.pop("relatedTransactionIDs", None))
        error_code = d.pop("errorCode", None)
        error_message = d.pop("errorMessage", None)
        close_trade_response_404 = cls(
            order_reject_transaction=order_reject_transaction,
            last_transaction_id=last_transaction_id,
            related_transaction_i_ds=related_transaction_i_ds,
            error_code=error_code,
            error_message=error_message,
        )
        close_trade_response_404.additional_properties = d
        return close_trade_response_404

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
