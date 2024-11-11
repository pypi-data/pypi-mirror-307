from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .market_order_reject_transaction import MarketOrderRejectTransaction
from typing import List, Optional, Type, TypeVar, cast

T = TypeVar("T", bound="ClosePositionResponse404")


@dataclasses.dataclass
class ClosePositionResponse404:
    """Attributes:
    long_order_reject_transaction (Optional[MarketOrderRejectTransaction]): A MarketOrderRejectTransaction
        represents the rejection of the creation of a Market Order.
    short_order_reject_transaction (Optional[MarketOrderRejectTransaction]): A MarketOrderRejectTransaction
        represents the rejection of the creation of a Market Order.
    related_transaction_i_ds (Optional[List[str]]): The IDs of all Transactions that were created while
        satisfying the request. Only present if the Account exists.
    last_transaction_id (Optional[str]): The ID of the most recent Transaction created for the Account. Only
        present if the Account exists.
    error_code (Optional[str]): The code of the error that has occurred. This field may not be returned for some
        errors.
    error_message (Optional[str]): The human-readable description of the error that has occurred."""

    long_order_reject_transaction: Optional["MarketOrderRejectTransaction"]
    short_order_reject_transaction: Optional["MarketOrderRejectTransaction"]
    related_transaction_i_ds: Optional[List[str]]
    last_transaction_id: Optional[str]
    error_code: Optional[str]
    error_message: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .market_order_reject_transaction import MarketOrderRejectTransaction

        d = src_dict.copy()
        _long_order_reject_transaction = d.pop("longOrderRejectTransaction", None)
        long_order_reject_transaction: Optional[MarketOrderRejectTransaction]
        if _long_order_reject_transaction is None:
            long_order_reject_transaction = None
        else:
            long_order_reject_transaction = MarketOrderRejectTransaction.from_dict(
                _long_order_reject_transaction
            )
        _short_order_reject_transaction = d.pop("shortOrderRejectTransaction", None)
        short_order_reject_transaction: Optional[MarketOrderRejectTransaction]
        if _short_order_reject_transaction is None:
            short_order_reject_transaction = None
        else:
            short_order_reject_transaction = MarketOrderRejectTransaction.from_dict(
                _short_order_reject_transaction
            )
        related_transaction_i_ds = cast(List[str], d.pop("relatedTransactionIDs", None))
        last_transaction_id = d.pop("lastTransactionID", None)
        error_code = d.pop("errorCode", None)
        error_message = d.pop("errorMessage", None)
        close_position_response_404 = cls(
            long_order_reject_transaction=long_order_reject_transaction,
            short_order_reject_transaction=short_order_reject_transaction,
            related_transaction_i_ds=related_transaction_i_ds,
            last_transaction_id=last_transaction_id,
            error_code=error_code,
            error_message=error_message,
        )
        close_position_response_404.additional_properties = d
        return close_position_response_404

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
