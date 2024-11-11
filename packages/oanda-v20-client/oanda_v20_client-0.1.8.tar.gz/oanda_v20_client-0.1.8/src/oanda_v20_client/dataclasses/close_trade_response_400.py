from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .market_order_reject_transaction import MarketOrderRejectTransaction
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="CloseTradeResponse400")


@dataclasses.dataclass
class CloseTradeResponse400:
    """Attributes:
    order_reject_transaction (Union[Unset, MarketOrderRejectTransaction]): A MarketOrderRejectTransaction represents
        the rejection of the creation of a Market Order.
    error_code (Union[Unset, str]): The code of the error that has occurred. This field may not be returned for some
        errors.
    error_message (Union[Unset, str]): The human-readable description of the error that has occurred."""

    order_reject_transaction: Optional["MarketOrderRejectTransaction"]
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
        error_code = d.pop("errorCode", None)
        error_message = d.pop("errorMessage", None)
        close_trade_response_400 = cls(
            order_reject_transaction=order_reject_transaction,
            error_code=error_code,
            error_message=error_message,
        )
        close_trade_response_400.additional_properties = d
        return close_trade_response_400

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
