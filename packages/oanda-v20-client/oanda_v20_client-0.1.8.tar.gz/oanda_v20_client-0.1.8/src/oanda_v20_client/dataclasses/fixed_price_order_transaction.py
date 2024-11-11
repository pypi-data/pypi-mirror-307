from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from .fixed_price_order_transaction_position_fill import (
    FixedPriceOrderTransactionPositionFill,
)
from .fixed_price_order_transaction_position_fill import (
    check_fixed_price_order_transaction_position_fill,
)
from .fixed_price_order_transaction_reason import FixedPriceOrderTransactionReason
from .fixed_price_order_transaction_reason import (
    check_fixed_price_order_transaction_reason,
)
from .fixed_price_order_transaction_type import FixedPriceOrderTransactionType
from .fixed_price_order_transaction_type import check_fixed_price_order_transaction_type
from .stop_loss_details import StopLossDetails
from .take_profit_details import TakeProfitDetails
from .trailing_stop_loss_details import TrailingStopLossDetails
from types import Unset
from typing import Optional, Type, TypeVar

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

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .stop_loss_details import StopLossDetails
        from .trailing_stop_loss_details import TrailingStopLossDetails
        from .take_profit_details import TakeProfitDetails
        from .client_extensions import ClientExtensions

        d = src_dict.copy()
        id = d.pop("id", None)
        time = d.pop("time", None)
        user_id = d.pop("userID", None)
        account_id = d.pop("accountID", None)
        batch_id = d.pop("batchID", None)
        request_id = d.pop("requestID", None)
        _type = d.pop("type", None)
        type: Optional[FixedPriceOrderTransactionType]
        if _type is None:
            type = None
        else:
            type = check_fixed_price_order_transaction_type(_type)
        instrument = d.pop("instrument", None)
        units = d.pop("units", None)
        price = d.pop("price", None)
        _position_fill = d.pop("positionFill", None)
        position_fill: Optional[FixedPriceOrderTransactionPositionFill]
        if isinstance(_position_fill, Unset):
            position_fill = None
        else:
            position_fill = check_fixed_price_order_transaction_position_fill(
                _position_fill
            )
        trade_state = d.pop("tradeState", None)
        _reason = d.pop("reason", None)
        reason: Optional[FixedPriceOrderTransactionReason]
        if isinstance(_reason, Unset):
            reason = None
        else:
            reason = check_fixed_price_order_transaction_reason(_reason)
        _client_extensions = d.pop("clientExtensions", None)
        client_extensions: Optional[ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = None
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)
        _take_profit_on_fill = d.pop("takeProfitOnFill", None)
        take_profit_on_fill: Optional[TakeProfitDetails]
        if isinstance(_take_profit_on_fill, Unset):
            take_profit_on_fill = None
        else:
            take_profit_on_fill = TakeProfitDetails.from_dict(_take_profit_on_fill)
        _stop_loss_on_fill = d.pop("stopLossOnFill", None)
        stop_loss_on_fill: Optional[StopLossDetails]
        if isinstance(_stop_loss_on_fill, Unset):
            stop_loss_on_fill = None
        else:
            stop_loss_on_fill = StopLossDetails.from_dict(_stop_loss_on_fill)
        _trailing_stop_loss_on_fill = d.pop("trailingStopLossOnFill", None)
        trailing_stop_loss_on_fill: Optional[TrailingStopLossDetails]
        if isinstance(_trailing_stop_loss_on_fill, Unset):
            trailing_stop_loss_on_fill = None
        else:
            trailing_stop_loss_on_fill = TrailingStopLossDetails.from_dict(
                _trailing_stop_loss_on_fill
            )
        _trade_client_extensions = d.pop("tradeClientExtensions", None)
        trade_client_extensions: Optional[ClientExtensions]
        if isinstance(_trade_client_extensions, Unset):
            trade_client_extensions = None
        else:
            trade_client_extensions = ClientExtensions.from_dict(
                _trade_client_extensions
            )
        fixed_price_order_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
            instrument=instrument,
            units=units,
            price=price,
            position_fill=position_fill,
            trade_state=trade_state,
            reason=reason,
            client_extensions=client_extensions,
            take_profit_on_fill=take_profit_on_fill,
            stop_loss_on_fill=stop_loss_on_fill,
            trailing_stop_loss_on_fill=trailing_stop_loss_on_fill,
            trade_client_extensions=trade_client_extensions,
        )
        fixed_price_order_transaction.additional_properties = d
        return fixed_price_order_transaction

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
