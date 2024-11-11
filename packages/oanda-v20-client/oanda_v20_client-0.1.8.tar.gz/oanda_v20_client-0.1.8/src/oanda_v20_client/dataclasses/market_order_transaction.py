from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from .market_order_delayed_trade_close import MarketOrderDelayedTradeClose
from .market_order_margin_closeout import MarketOrderMarginCloseout
from .market_order_position_closeout import MarketOrderPositionCloseout
from .market_order_trade_close import MarketOrderTradeClose
from .market_order_transaction_position_fill import MarketOrderTransactionPositionFill
from .market_order_transaction_position_fill import (
    check_market_order_transaction_position_fill,
)
from .market_order_transaction_reason import MarketOrderTransactionReason
from .market_order_transaction_reason import check_market_order_transaction_reason
from .market_order_transaction_time_in_force import MarketOrderTransactionTimeInForce
from .market_order_transaction_time_in_force import (
    check_market_order_transaction_time_in_force,
)
from .market_order_transaction_type import MarketOrderTransactionType
from .market_order_transaction_type import check_market_order_transaction_type
from .stop_loss_details import StopLossDetails
from .take_profit_details import TakeProfitDetails
from .trailing_stop_loss_details import TrailingStopLossDetails
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="MarketOrderTransaction")


@dataclasses.dataclass
class MarketOrderTransaction:
    """A MarketOrderTransaction represents the creation of a Market Order in the user's account. A Market Order is an Order
    that is filled immediately at the current market price.
    Market Orders can be specialized when they are created to accomplish a specific task: to close a Trade, to closeout
    a Position or to particiate in in a Margin closeout.

        Attributes:
            id (Union[Unset, str]): The Transaction's Identifier.
            time (Union[Unset, str]): The date/time when the Transaction was created.
            user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
            account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
            batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
                batch are applied to the Account simultaneously.
            request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
            type (Union[Unset, MarketOrderTransactionType]): The Type of the Transaction. Always set to "MARKET_ORDER" in a
                MarketOrderTransaction.
            instrument (Union[Unset, str]): The Market Order's Instrument.
            units (Union[Unset, str]): The quantity requested to be filled by the Market Order. A posititive number of units
                results in a long Order, and a negative number of units results in a short Order.
            time_in_force (Union[Unset, MarketOrderTransactionTimeInForce]): The time-in-force requested for the Market
                Order. Restricted to FOK or IOC for a MarketOrder.
            price_bound (Union[Unset, str]): The worst price that the client is willing to have the Market Order filled at.
            position_fill (Union[Unset, MarketOrderTransactionPositionFill]): Specification of how Positions in the Account
                are modified when the Order is filled.
            trade_close (Union[Unset, MarketOrderTradeClose]): A MarketOrderTradeClose specifies the extensions to a Market
                Order that has been created specifically to close a Trade.
            long_position_closeout (Union[Unset, MarketOrderPositionCloseout]): A MarketOrderPositionCloseout specifies the
                extensions to a Market Order when it has been created to closeout a specific Position.
            short_position_closeout (Union[Unset, MarketOrderPositionCloseout]): A MarketOrderPositionCloseout specifies the
                extensions to a Market Order when it has been created to closeout a specific Position.
            margin_closeout (Union[Unset, MarketOrderMarginCloseout]): Details for the Market Order extensions specific to a
                Market Order placed that is part of a Market Order Margin Closeout in a client's account
            delayed_trade_close (Union[Unset, MarketOrderDelayedTradeClose]): Details for the Market Order extensions
                specific to a Market Order placed with the intent of fully closing a specific open trade that should have
                already been closed but wasn't due to halted market conditions
            reason (Union[Unset, MarketOrderTransactionReason]): The reason that the Market Order was created
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
    type: Optional[MarketOrderTransactionType]
    instrument: Optional[str]
    units: Optional[str]
    time_in_force: Optional[MarketOrderTransactionTimeInForce]
    price_bound: Optional[str]
    position_fill: Optional[MarketOrderTransactionPositionFill]
    trade_close: Optional["MarketOrderTradeClose"]
    long_position_closeout: Optional["MarketOrderPositionCloseout"]
    short_position_closeout: Optional["MarketOrderPositionCloseout"]
    margin_closeout: Optional["MarketOrderMarginCloseout"]
    delayed_trade_close: Optional["MarketOrderDelayedTradeClose"]
    reason: Optional[MarketOrderTransactionReason]
    client_extensions: Optional["ClientExtensions"]
    take_profit_on_fill: Optional["TakeProfitDetails"]
    stop_loss_on_fill: Optional["StopLossDetails"]
    trailing_stop_loss_on_fill: Optional["TrailingStopLossDetails"]
    trade_client_extensions: Optional["ClientExtensions"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .market_order_margin_closeout import MarketOrderMarginCloseout
        from .market_order_trade_close import MarketOrderTradeClose
        from .stop_loss_details import StopLossDetails
        from .take_profit_details import TakeProfitDetails
        from .client_extensions import ClientExtensions
        from .trailing_stop_loss_details import TrailingStopLossDetails
        from .market_order_delayed_trade_close import MarketOrderDelayedTradeClose
        from .market_order_position_closeout import MarketOrderPositionCloseout

        d = src_dict.copy()
        id = d.pop("id", None)
        time = d.pop("time", None)
        user_id = d.pop("userID", None)
        account_id = d.pop("accountID", None)
        batch_id = d.pop("batchID", None)
        request_id = d.pop("requestID", None)
        _type = d.pop("type", None)
        type: Optional[MarketOrderTransactionType]
        if _type is None:
            type = None
        else:
            type = check_market_order_transaction_type(_type)
        instrument = d.pop("instrument", None)
        units = d.pop("units", None)
        _time_in_force = d.pop("timeInForce", None)
        time_in_force: Optional[MarketOrderTransactionTimeInForce]
        if isinstance(_time_in_force, Unset):
            time_in_force = None
        else:
            time_in_force = check_market_order_transaction_time_in_force(_time_in_force)
        price_bound = d.pop("priceBound", None)
        _position_fill = d.pop("positionFill", None)
        position_fill: Optional[MarketOrderTransactionPositionFill]
        if isinstance(_position_fill, Unset):
            position_fill = None
        else:
            position_fill = check_market_order_transaction_position_fill(_position_fill)
        _trade_close = d.pop("tradeClose", None)
        trade_close: Optional[MarketOrderTradeClose]
        if isinstance(_trade_close, Unset):
            trade_close = None
        else:
            trade_close = MarketOrderTradeClose.from_dict(_trade_close)
        _long_position_closeout = d.pop("longPositionCloseout", None)
        long_position_closeout: Optional[MarketOrderPositionCloseout]
        if isinstance(_long_position_closeout, Unset):
            long_position_closeout = None
        else:
            long_position_closeout = MarketOrderPositionCloseout.from_dict(
                _long_position_closeout
            )
        _short_position_closeout = d.pop("shortPositionCloseout", None)
        short_position_closeout: Optional[MarketOrderPositionCloseout]
        if isinstance(_short_position_closeout, Unset):
            short_position_closeout = None
        else:
            short_position_closeout = MarketOrderPositionCloseout.from_dict(
                _short_position_closeout
            )
        _margin_closeout = d.pop("marginCloseout", None)
        margin_closeout: Optional[MarketOrderMarginCloseout]
        if isinstance(_margin_closeout, Unset):
            margin_closeout = None
        else:
            margin_closeout = MarketOrderMarginCloseout.from_dict(_margin_closeout)
        _delayed_trade_close = d.pop("delayedTradeClose", None)
        delayed_trade_close: Optional[MarketOrderDelayedTradeClose]
        if isinstance(_delayed_trade_close, Unset):
            delayed_trade_close = None
        else:
            delayed_trade_close = MarketOrderDelayedTradeClose.from_dict(
                _delayed_trade_close
            )
        _reason = d.pop("reason", None)
        reason: Optional[MarketOrderTransactionReason]
        if isinstance(_reason, Unset):
            reason = None
        else:
            reason = check_market_order_transaction_reason(_reason)
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
        market_order_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
            instrument=instrument,
            units=units,
            time_in_force=time_in_force,
            price_bound=price_bound,
            position_fill=position_fill,
            trade_close=trade_close,
            long_position_closeout=long_position_closeout,
            short_position_closeout=short_position_closeout,
            margin_closeout=margin_closeout,
            delayed_trade_close=delayed_trade_close,
            reason=reason,
            client_extensions=client_extensions,
            take_profit_on_fill=take_profit_on_fill,
            stop_loss_on_fill=stop_loss_on_fill,
            trailing_stop_loss_on_fill=trailing_stop_loss_on_fill,
            trade_client_extensions=trade_client_extensions,
        )
        market_order_transaction.additional_properties = d
        return market_order_transaction

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
