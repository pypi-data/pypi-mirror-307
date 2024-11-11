from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_extensions import ClientExtensions
from .market_if_touched_order_reject_transaction_position_fill import (
    MarketIfTouchedOrderRejectTransactionPositionFill,
)
from .market_if_touched_order_reject_transaction_position_fill import (
    check_market_if_touched_order_reject_transaction_position_fill,
)
from .market_if_touched_order_reject_transaction_reason import (
    MarketIfTouchedOrderRejectTransactionReason,
)
from .market_if_touched_order_reject_transaction_reason import (
    check_market_if_touched_order_reject_transaction_reason,
)
from .market_if_touched_order_reject_transaction_reject_reason import (
    MarketIfTouchedOrderRejectTransactionRejectReason,
)
from .market_if_touched_order_reject_transaction_reject_reason import (
    check_market_if_touched_order_reject_transaction_reject_reason,
)
from .market_if_touched_order_reject_transaction_time_in_force import (
    MarketIfTouchedOrderRejectTransactionTimeInForce,
)
from .market_if_touched_order_reject_transaction_time_in_force import (
    check_market_if_touched_order_reject_transaction_time_in_force,
)
from .market_if_touched_order_reject_transaction_trigger_condition import (
    MarketIfTouchedOrderRejectTransactionTriggerCondition,
)
from .market_if_touched_order_reject_transaction_trigger_condition import (
    check_market_if_touched_order_reject_transaction_trigger_condition,
)
from .market_if_touched_order_reject_transaction_type import (
    MarketIfTouchedOrderRejectTransactionType,
)
from .market_if_touched_order_reject_transaction_type import (
    check_market_if_touched_order_reject_transaction_type,
)
from .stop_loss_details import StopLossDetails
from .take_profit_details import TakeProfitDetails
from .trailing_stop_loss_details import TrailingStopLossDetails
from types import Unset
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="MarketIfTouchedOrderRejectTransaction")


@dataclasses.dataclass
class MarketIfTouchedOrderRejectTransaction:
    """A MarketIfTouchedOrderRejectTransaction represents the rejection of the creation of a MarketIfTouched Order.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, MarketIfTouchedOrderRejectTransactionType]): The Type of the Transaction. Always set to
            "MARKET_IF_TOUCHED_ORDER_REJECT" in a MarketIfTouchedOrderRejectTransaction.
        instrument (Union[Unset, str]): The MarketIfTouched Order's Instrument.
        units (Union[Unset, str]): The quantity requested to be filled by the MarketIfTouched Order. A posititive number
            of units results in a long Order, and a negative number of units results in a short Order.
        price (Union[Unset, str]): The price threshold specified for the MarketIfTouched Order. The MarketIfTouched
            Order will only be filled by a market price that crosses this price from the direction of the market price at
            the time when the Order was created (the initialMarketPrice). Depending on the value of the Order's price and
            initialMarketPrice, the MarketIfTouchedOrder will behave like a Limit or a Stop Order.
        price_bound (Union[Unset, str]): The worst market price that may be used to fill this MarketIfTouched Order.
        time_in_force (Union[Unset, MarketIfTouchedOrderRejectTransactionTimeInForce]): The time-in-force requested for
            the MarketIfTouched Order. Restricted to "GTC", "GFD" and "GTD" for MarketIfTouched Orders.
        gtd_time (Union[Unset, str]): The date/time when the MarketIfTouched Order will be cancelled if its timeInForce
            is "GTD".
        position_fill (Union[Unset, MarketIfTouchedOrderRejectTransactionPositionFill]): Specification of how Positions
            in the Account are modified when the Order is filled.
        trigger_condition (Union[Unset, MarketIfTouchedOrderRejectTransactionTriggerCondition]): Specification of which
            price component should be used when determining if an Order should be triggered and filled. This allows Orders
            to be triggered based on the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid
            for buy) price depending on the desired behaviour. Orders are always filled using their default price component.
            This feature is only provided through the REST API. Clients who choose to specify a non-default trigger
            condition will not see it reflected in any of OANDA's proprietary or partner trading platforms, their
            transaction history or their account statements. OANDA platforms always assume that an Order's trigger condition
            is set to the default value when indicating the distance from an Order's trigger price, and will always provide
            the default trigger condition when creating or modifying an Order.
            A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition
            value must either be "DEFAULT", or the "natural" trigger side "DEFAULT" results in. So for a Stop Loss Order for
            a long trade valid values are "DEFAULT" and "BID", and for short trades "DEFAULT" and "ASK" are valid.
        reason (Union[Unset, MarketIfTouchedOrderRejectTransactionReason]): The reason that the Market-if-touched Order
            was initiated
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
            your account is associated with MT4.
        intended_replaces_order_id (Union[Unset, str]): The ID of the Order that this Order was intended to replace
            (only provided if this Order was intended to replace an existing Order).
        reject_reason (Union[Unset, MarketIfTouchedOrderRejectTransactionRejectReason]): The reason that the Reject
            Transaction was created"""

    id: Optional[str]
    time: Optional[str]
    user_id: Optional[int]
    account_id: Optional[str]
    batch_id: Optional[str]
    request_id: Optional[str]
    type: Optional[MarketIfTouchedOrderRejectTransactionType]
    instrument: Optional[str]
    units: Optional[str]
    price: Optional[str]
    price_bound: Optional[str]
    time_in_force: Optional[MarketIfTouchedOrderRejectTransactionTimeInForce]
    gtd_time: Optional[str]
    position_fill: Optional[MarketIfTouchedOrderRejectTransactionPositionFill]
    trigger_condition: Optional[MarketIfTouchedOrderRejectTransactionTriggerCondition]
    reason: Optional[MarketIfTouchedOrderRejectTransactionReason]
    client_extensions: Optional["ClientExtensions"]
    take_profit_on_fill: Optional["TakeProfitDetails"]
    stop_loss_on_fill: Optional["StopLossDetails"]
    trailing_stop_loss_on_fill: Optional["TrailingStopLossDetails"]
    trade_client_extensions: Optional["ClientExtensions"]
    intended_replaces_order_id: Optional[str]
    reject_reason: Optional[MarketIfTouchedOrderRejectTransactionRejectReason]

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
        type: Optional[MarketIfTouchedOrderRejectTransactionType]
        if _type is None:
            type = None
        else:
            type = check_market_if_touched_order_reject_transaction_type(_type)
        instrument = d.pop("instrument", None)
        units = d.pop("units", None)
        price = d.pop("price", None)
        price_bound = d.pop("priceBound", None)
        _time_in_force = d.pop("timeInForce", None)
        time_in_force: Optional[MarketIfTouchedOrderRejectTransactionTimeInForce]
        if isinstance(_time_in_force, Unset):
            time_in_force = None
        else:
            time_in_force = (
                check_market_if_touched_order_reject_transaction_time_in_force(
                    _time_in_force
                )
            )
        gtd_time = d.pop("gtdTime", None)
        _position_fill = d.pop("positionFill", None)
        position_fill: Optional[MarketIfTouchedOrderRejectTransactionPositionFill]
        if isinstance(_position_fill, Unset):
            position_fill = None
        else:
            position_fill = (
                check_market_if_touched_order_reject_transaction_position_fill(
                    _position_fill
                )
            )
        _trigger_condition = d.pop("triggerCondition", None)
        trigger_condition: Optional[
            MarketIfTouchedOrderRejectTransactionTriggerCondition
        ]
        if isinstance(_trigger_condition, Unset):
            trigger_condition = None
        else:
            trigger_condition = (
                check_market_if_touched_order_reject_transaction_trigger_condition(
                    _trigger_condition
                )
            )
        _reason = d.pop("reason", None)
        reason: Optional[MarketIfTouchedOrderRejectTransactionReason]
        if isinstance(_reason, Unset):
            reason = None
        else:
            reason = check_market_if_touched_order_reject_transaction_reason(_reason)
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
        intended_replaces_order_id = d.pop("intendedReplacesOrderID", None)
        _reject_reason = d.pop("rejectReason", None)
        reject_reason: Optional[MarketIfTouchedOrderRejectTransactionRejectReason]
        if isinstance(_reject_reason, Unset):
            reject_reason = None
        else:
            reject_reason = (
                check_market_if_touched_order_reject_transaction_reject_reason(
                    _reject_reason
                )
            )
        market_if_touched_order_reject_transaction = cls(
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
            price_bound=price_bound,
            time_in_force=time_in_force,
            gtd_time=gtd_time,
            position_fill=position_fill,
            trigger_condition=trigger_condition,
            reason=reason,
            client_extensions=client_extensions,
            take_profit_on_fill=take_profit_on_fill,
            stop_loss_on_fill=stop_loss_on_fill,
            trailing_stop_loss_on_fill=trailing_stop_loss_on_fill,
            trade_client_extensions=trade_client_extensions,
            intended_replaces_order_id=intended_replaces_order_id,
            reject_reason=reject_reason,
        )
        market_if_touched_order_reject_transaction.additional_properties = d
        return market_if_touched_order_reject_transaction

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
