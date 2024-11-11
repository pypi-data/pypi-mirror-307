from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .client_extensions import ClientExtensions
from .fixed_price_order_transaction_position_fill import (
    FixedPriceOrderTransactionPositionFill,
)
from .fixed_price_order_transaction_reason import FixedPriceOrderTransactionReason
from .fixed_price_order_transaction_type import FixedPriceOrderTransactionType
from .stop_loss_details import StopLossDetails
from .take_profit_details import TakeProfitDetails
from .trailing_stop_loss_details import TrailingStopLossDetails
from typing import Optional, TypeVar

T = TypeVar("T", bound="FixedPriceOrderTransaction")


@dataclasses.dataclass
class FixedPriceOrderTransaction:
    """A FixedPriceOrderTransaction represents the creation of a Fixed Price Order in the user's account. A Fixed Price
    Order is an Order that is filled immediately at a specified price.

        Attributes:
            id (Union[Unset, str]): The Transaction's Identifier.
            time (Union[Unset, str]): The date/time when the Transaction was created.
            user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
            account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
            batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
                batch are applied to the Account simultaneously.
            request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
            type (Union[Unset, FixedPriceOrderTransactionType]): The Type of the Transaction. Always set to
                "FIXED_PRICE_ORDER" in a FixedPriceOrderTransaction.
            instrument (Union[Unset, str]): The Fixed Price Order's Instrument.
            units (Union[Unset, str]): The quantity requested to be filled by the Fixed Price Order. A posititive number of
                units results in a long Order, and a negative number of units results in a short Order.
            price (Union[Unset, str]): The price specified for the Fixed Price Order. This price is the exact price that the
                Fixed Price Order will be filled at.
            position_fill (Union[Unset, FixedPriceOrderTransactionPositionFill]): Specification of how Positions in the
                Account are modified when the Order is filled.
            trade_state (Union[Unset, str]): The state that the trade resulting from the Fixed Price Order should be set to.
            reason (Union[Unset, FixedPriceOrderTransactionReason]): The reason that the Fixed Price Order was created
            client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
                clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
                your account is associated with MT4.
            take_profit_on_fill (Union[Unset, TakeProfitDetails]): TakeProfitDetails specifies the details of a Take Profit
                Order to be created on behalf of a client. This may happen when an Order is filled that opens a Trade requiring
                a Take Profit, or when a Trade's dependent Take Profit Order is modified directly through the Trade.
            stop_loss_on_fill (Union[Unset, StopLossDetails]): StopLossDetails specifies the details of a Stop Loss Order to
                be created on behalf of a client. This may happen when an Order is filled that opens a Trade requiring a Stop
                Loss, or when a Trade's dependent Stop Loss Order is modified directly through the Trade.
            trailing_stop_loss_on_fill (Union[Unset, TrailingStopLossDetails]): TrailingStopLossDetails specifies the
                details of a Trailing Stop Loss Order to be created on behalf of a client. This may happen when an Order is
                filled that opens a Trade requiring a Trailing Stop Loss, or when a Trade's dependent Trailing Stop Loss Order
                is modified directly through the Trade.
            trade_client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
                clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
                your account is associated with MT4."""

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]
    type: Optional[FixedPriceOrderTransactionType]
    instrument: Optional[str]
    units: Optional[str]
    price: Optional[str]
    position_fill: Optional[FixedPriceOrderTransactionPositionFill]
    trade_state: Optional[str]
    reason: Optional[FixedPriceOrderTransactionReason]
    client_extensions: Optional["ClientExtensions"]
    take_profit_on_fill: Optional["TakeProfitDetails"]
    stop_loss_on_fill: Optional["StopLossDetails"]
    trailing_stop_loss_on_fill: Optional["TrailingStopLossDetails"]
    trade_client_extensions: Optional["ClientExtensions"]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FixedPriceOrderTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
