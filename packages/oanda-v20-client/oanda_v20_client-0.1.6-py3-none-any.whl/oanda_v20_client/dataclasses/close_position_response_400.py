from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .market_order_reject_transaction import MarketOrderRejectTransaction
from typing import List, Optional, TypeVar

T = TypeVar("T", bound="ClosePositionResponse400")


@dataclasses.dataclass
class ClosePositionResponse400:
    """Attributes:
    long_order_reject_transaction (Union[Unset, MarketOrderRejectTransaction]): A MarketOrderRejectTransaction
        represents the rejection of the creation of a Market Order.
    short_order_reject_transaction (Union[Unset, MarketOrderRejectTransaction]): A MarketOrderRejectTransaction
        represents the rejection of the creation of a Market Order.
    related_transaction_i_ds (Union[Unset, List[str]]): The IDs of all Transactions that were created while
        satisfying the request.
    last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account
    error_code (Union[Unset, str]): The code of the error that has occurred. This field may not be returned for some
        errors.
    error_message (Union[Unset, str]): The human-readable description of the error that has occurred."""

    long_order_reject_transaction: Optional["MarketOrderRejectTransaction"]
    short_order_reject_transaction: Optional["MarketOrderRejectTransaction"]
    related_transaction_i_ds: Optional[List[str]]
    last_transaction_id: Optional[str]
    error_code: Optional[str]
    error_message: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClosePositionResponse400":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
