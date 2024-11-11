from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.limit_order_transaction_position_fill import (
    check_limit_order_transaction_position_fill,
)
from ..models.limit_order_transaction_position_fill import (
    LimitOrderTransactionPositionFill,
)
from ..models.limit_order_transaction_reason import check_limit_order_transaction_reason
from ..models.limit_order_transaction_reason import LimitOrderTransactionReason
from ..models.limit_order_transaction_time_in_force import (
    check_limit_order_transaction_time_in_force,
)
from ..models.limit_order_transaction_time_in_force import (
    LimitOrderTransactionTimeInForce,
)
from ..models.limit_order_transaction_trigger_condition import (
    check_limit_order_transaction_trigger_condition,
)
from ..models.limit_order_transaction_trigger_condition import (
    LimitOrderTransactionTriggerCondition,
)
from ..models.limit_order_transaction_type import check_limit_order_transaction_type
from ..models.limit_order_transaction_type import LimitOrderTransactionType
from typing import Union

if TYPE_CHECKING:
    from ..models.client_extensions import ClientExtensions
    from ..models.stop_loss_details import StopLossDetails
    from ..models.trailing_stop_loss_details import TrailingStopLossDetails
    from ..models.take_profit_details import TakeProfitDetails


T = TypeVar("T", bound="LimitOrderTransaction")


@_attrs_define
class LimitOrderTransaction:
    """A LimitOrderTransaction represents the creation of a Limit Order in the user's Account.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, LimitOrderTransactionType]): The Type of the Transaction. Always set to "LIMIT_ORDER" in a
            LimitOrderTransaction.
        instrument (Union[Unset, str]): The Limit Order's Instrument.
        units (Union[Unset, str]): The quantity requested to be filled by the Limit Order. A posititive number of units
            results in a long Order, and a negative number of units results in a short Order.
        price (Union[Unset, str]): The price threshold specified for the Limit Order. The Limit Order will only be
            filled by a market price that is equal to or better than this price.
        time_in_force (Union[Unset, LimitOrderTransactionTimeInForce]): The time-in-force requested for the Limit Order.
        gtd_time (Union[Unset, str]): The date/time when the Limit Order will be cancelled if its timeInForce is "GTD".
        position_fill (Union[Unset, LimitOrderTransactionPositionFill]): Specification of how Positions in the Account
            are modified when the Order is filled.
        trigger_condition (Union[Unset, LimitOrderTransactionTriggerCondition]): Specification of which price component
            should be used when determining if an Order should be triggered and filled. This allows Orders to be triggered
            based on the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid for buy) price
            depending on the desired behaviour. Orders are always filled using their default price component.
            This feature is only provided through the REST API. Clients who choose to specify a non-default trigger
            condition will not see it reflected in any of OANDA's proprietary or partner trading platforms, their
            transaction history or their account statements. OANDA platforms always assume that an Order's trigger condition
            is set to the default value when indicating the distance from an Order's trigger price, and will always provide
            the default trigger condition when creating or modifying an Order.
            A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition
            value must either be "DEFAULT", or the "natural" trigger side "DEFAULT" results in. So for a Stop Loss Order for
            a long trade valid values are "DEFAULT" and "BID", and for short trades "DEFAULT" and "ASK" are valid.
        reason (Union[Unset, LimitOrderTransactionReason]): The reason that the Limit Order was initiated
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
        replaces_order_id (Union[Unset, str]): The ID of the Order that this Order replaces (only provided if this Order
            replaces an existing Order).
        cancelling_transaction_id (Union[Unset, str]): The ID of the Transaction that cancels the replaced Order (only
            provided if this Order replaces an existing Order).
    """

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, LimitOrderTransactionType] = UNSET
    instrument: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    time_in_force: Union[Unset, LimitOrderTransactionTimeInForce] = UNSET
    gtd_time: Union[Unset, str] = UNSET
    position_fill: Union[Unset, LimitOrderTransactionPositionFill] = UNSET
    trigger_condition: Union[Unset, LimitOrderTransactionTriggerCondition] = UNSET
    reason: Union[Unset, LimitOrderTransactionReason] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    take_profit_on_fill: Union[Unset, "TakeProfitDetails"] = UNSET
    stop_loss_on_fill: Union[Unset, "StopLossDetails"] = UNSET
    trailing_stop_loss_on_fill: Union[Unset, "TrailingStopLossDetails"] = UNSET
    trade_client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    replaces_order_id: Union[Unset, str] = UNSET
    cancelling_transaction_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        time = self.time

        user_id = self.user_id

        account_id = self.account_id

        batch_id = self.batch_id

        request_id = self.request_id

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type

        instrument = self.instrument

        units = self.units

        price = self.price

        time_in_force: Union[Unset, str] = UNSET
        if not isinstance(self.time_in_force, Unset):
            time_in_force = self.time_in_force

        gtd_time = self.gtd_time

        position_fill: Union[Unset, str] = UNSET
        if not isinstance(self.position_fill, Unset):
            position_fill = self.position_fill

        trigger_condition: Union[Unset, str] = UNSET
        if not isinstance(self.trigger_condition, Unset):
            trigger_condition = self.trigger_condition

        reason: Union[Unset, str] = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason

        client_extensions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.client_extensions, Unset):
            client_extensions = self.client_extensions.to_dict()

        take_profit_on_fill: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.take_profit_on_fill, Unset):
            take_profit_on_fill = self.take_profit_on_fill.to_dict()

        stop_loss_on_fill: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stop_loss_on_fill, Unset):
            stop_loss_on_fill = self.stop_loss_on_fill.to_dict()

        trailing_stop_loss_on_fill: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.trailing_stop_loss_on_fill, Unset):
            trailing_stop_loss_on_fill = self.trailing_stop_loss_on_fill.to_dict()

        trade_client_extensions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.trade_client_extensions, Unset):
            trade_client_extensions = self.trade_client_extensions.to_dict()

        replaces_order_id = self.replaces_order_id

        cancelling_transaction_id = self.cancelling_transaction_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if time is not UNSET:
            field_dict["time"] = time
        if user_id is not UNSET:
            field_dict["userID"] = user_id
        if account_id is not UNSET:
            field_dict["accountID"] = account_id
        if batch_id is not UNSET:
            field_dict["batchID"] = batch_id
        if request_id is not UNSET:
            field_dict["requestID"] = request_id
        if type is not UNSET:
            field_dict["type"] = type
        if instrument is not UNSET:
            field_dict["instrument"] = instrument
        if units is not UNSET:
            field_dict["units"] = units
        if price is not UNSET:
            field_dict["price"] = price
        if time_in_force is not UNSET:
            field_dict["timeInForce"] = time_in_force
        if gtd_time is not UNSET:
            field_dict["gtdTime"] = gtd_time
        if position_fill is not UNSET:
            field_dict["positionFill"] = position_fill
        if trigger_condition is not UNSET:
            field_dict["triggerCondition"] = trigger_condition
        if reason is not UNSET:
            field_dict["reason"] = reason
        if client_extensions is not UNSET:
            field_dict["clientExtensions"] = client_extensions
        if take_profit_on_fill is not UNSET:
            field_dict["takeProfitOnFill"] = take_profit_on_fill
        if stop_loss_on_fill is not UNSET:
            field_dict["stopLossOnFill"] = stop_loss_on_fill
        if trailing_stop_loss_on_fill is not UNSET:
            field_dict["trailingStopLossOnFill"] = trailing_stop_loss_on_fill
        if trade_client_extensions is not UNSET:
            field_dict["tradeClientExtensions"] = trade_client_extensions
        if replaces_order_id is not UNSET:
            field_dict["replacesOrderID"] = replaces_order_id
        if cancelling_transaction_id is not UNSET:
            field_dict["cancellingTransactionID"] = cancelling_transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.client_extensions import ClientExtensions
        from ..models.stop_loss_details import StopLossDetails
        from ..models.trailing_stop_loss_details import TrailingStopLossDetails
        from ..models.take_profit_details import TakeProfitDetails

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        time = d.pop("time", UNSET)

        user_id = d.pop("userID", UNSET)

        account_id = d.pop("accountID", UNSET)

        batch_id = d.pop("batchID", UNSET)

        request_id = d.pop("requestID", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, LimitOrderTransactionType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = check_limit_order_transaction_type(_type)

        instrument = d.pop("instrument", UNSET)

        units = d.pop("units", UNSET)

        price = d.pop("price", UNSET)

        _time_in_force = d.pop("timeInForce", UNSET)
        time_in_force: Union[Unset, LimitOrderTransactionTimeInForce]
        if isinstance(_time_in_force, Unset):
            time_in_force = UNSET
        else:
            time_in_force = check_limit_order_transaction_time_in_force(_time_in_force)

        gtd_time = d.pop("gtdTime", UNSET)

        _position_fill = d.pop("positionFill", UNSET)
        position_fill: Union[Unset, LimitOrderTransactionPositionFill]
        if isinstance(_position_fill, Unset):
            position_fill = UNSET
        else:
            position_fill = check_limit_order_transaction_position_fill(_position_fill)

        _trigger_condition = d.pop("triggerCondition", UNSET)
        trigger_condition: Union[Unset, LimitOrderTransactionTriggerCondition]
        if isinstance(_trigger_condition, Unset):
            trigger_condition = UNSET
        else:
            trigger_condition = check_limit_order_transaction_trigger_condition(
                _trigger_condition
            )

        _reason = d.pop("reason", UNSET)
        reason: Union[Unset, LimitOrderTransactionReason]
        if isinstance(_reason, Unset):
            reason = UNSET
        else:
            reason = check_limit_order_transaction_reason(_reason)

        _client_extensions = d.pop("clientExtensions", UNSET)
        client_extensions: Union[Unset, ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = UNSET
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)

        _take_profit_on_fill = d.pop("takeProfitOnFill", UNSET)
        take_profit_on_fill: Union[Unset, TakeProfitDetails]
        if isinstance(_take_profit_on_fill, Unset):
            take_profit_on_fill = UNSET
        else:
            take_profit_on_fill = TakeProfitDetails.from_dict(_take_profit_on_fill)

        _stop_loss_on_fill = d.pop("stopLossOnFill", UNSET)
        stop_loss_on_fill: Union[Unset, StopLossDetails]
        if isinstance(_stop_loss_on_fill, Unset):
            stop_loss_on_fill = UNSET
        else:
            stop_loss_on_fill = StopLossDetails.from_dict(_stop_loss_on_fill)

        _trailing_stop_loss_on_fill = d.pop("trailingStopLossOnFill", UNSET)
        trailing_stop_loss_on_fill: Union[Unset, TrailingStopLossDetails]
        if isinstance(_trailing_stop_loss_on_fill, Unset):
            trailing_stop_loss_on_fill = UNSET
        else:
            trailing_stop_loss_on_fill = TrailingStopLossDetails.from_dict(
                _trailing_stop_loss_on_fill
            )

        _trade_client_extensions = d.pop("tradeClientExtensions", UNSET)
        trade_client_extensions: Union[Unset, ClientExtensions]
        if isinstance(_trade_client_extensions, Unset):
            trade_client_extensions = UNSET
        else:
            trade_client_extensions = ClientExtensions.from_dict(
                _trade_client_extensions
            )

        replaces_order_id = d.pop("replacesOrderID", UNSET)

        cancelling_transaction_id = d.pop("cancellingTransactionID", UNSET)

        limit_order_transaction = cls(
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
            replaces_order_id=replaces_order_id,
            cancelling_transaction_id=cancelling_transaction_id,
        )

        limit_order_transaction.additional_properties = d
        return limit_order_transaction

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
