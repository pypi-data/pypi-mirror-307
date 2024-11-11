from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .market_order_reject_transaction import MarketOrderRejectTransaction
from typing import Optional, TypeVar

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

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CloseTradeResponse400":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
