from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .client_extensions import ClientExtensions
from .market_order_delayed_trade_close import MarketOrderDelayedTradeClose
from .market_order_margin_closeout import MarketOrderMarginCloseout
from .market_order_position_closeout import MarketOrderPositionCloseout
from .market_order_trade_close import MarketOrderTradeClose
from .market_order_transaction_position_fill import MarketOrderTransactionPositionFill
from .market_order_transaction_reason import MarketOrderTransactionReason
from .market_order_transaction_time_in_force import MarketOrderTransactionTimeInForce
from .market_order_transaction_type import MarketOrderTransactionType
from .stop_loss_details import StopLossDetails
from .take_profit_details import TakeProfitDetails
from .trailing_stop_loss_details import TrailingStopLossDetails
from types import UNSET, Unset
from typing import TypeVar
from typing import Union

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

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, MarketOrderTransactionType] = UNSET
    instrument: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET
    time_in_force: Union[Unset, MarketOrderTransactionTimeInForce] = UNSET
    price_bound: Union[Unset, str] = UNSET
    position_fill: Union[Unset, MarketOrderTransactionPositionFill] = UNSET
    trade_close: Union[Unset, "MarketOrderTradeClose"] = UNSET
    long_position_closeout: Union[Unset, "MarketOrderPositionCloseout"] = UNSET
    short_position_closeout: Union[Unset, "MarketOrderPositionCloseout"] = UNSET
    margin_closeout: Union[Unset, "MarketOrderMarginCloseout"] = UNSET
    delayed_trade_close: Union[Unset, "MarketOrderDelayedTradeClose"] = UNSET
    reason: Union[Unset, MarketOrderTransactionReason] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    take_profit_on_fill: Union[Unset, "TakeProfitDetails"] = UNSET
    stop_loss_on_fill: Union[Unset, "StopLossDetails"] = UNSET
    trailing_stop_loss_on_fill: Union[Unset, "TrailingStopLossDetails"] = UNSET
    trade_client_extensions: Union[Unset, "ClientExtensions"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MarketOrderTransaction":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
