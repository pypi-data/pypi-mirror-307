from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.take_profit_order_state import check_take_profit_order_state
from ..models.take_profit_order_state import TakeProfitOrderState
from ..models.take_profit_order_time_in_force import (
    check_take_profit_order_time_in_force,
)
from ..models.take_profit_order_time_in_force import TakeProfitOrderTimeInForce
from ..models.take_profit_order_trigger_condition import (
    check_take_profit_order_trigger_condition,
)
from ..models.take_profit_order_trigger_condition import TakeProfitOrderTriggerCondition
from ..models.take_profit_order_type import check_take_profit_order_type
from ..models.take_profit_order_type import TakeProfitOrderType
from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.client_extensions import ClientExtensions


T = TypeVar("T", bound="TakeProfitOrder")


@_attrs_define
class TakeProfitOrder:
    """A TakeProfitOrder is an order that is linked to an open Trade and created with a price threshold. The Order will be
    filled (closing the Trade) by the first price that is equal to or better than the threshold. A TakeProfitOrder
    cannot be used to open a new Position.

        Attributes:
            id (Union[Unset, str]): The Order's identifier, unique within the Order's Account.
            create_time (Union[Unset, str]): The time when the Order was created.
            state (Union[Unset, TakeProfitOrderState]): The current state of the Order.
            client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
                clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
                your account is associated with MT4.
            type (Union[Unset, TakeProfitOrderType]): The type of the Order. Always set to "TAKE_PROFIT" for Take Profit
                Orders.
            trade_id (Union[Unset, str]): The ID of the Trade to close when the price threshold is breached.
            client_trade_id (Union[Unset, str]): The client ID of the Trade to be closed when the price threshold is
                breached.
            price (Union[Unset, str]): The price threshold specified for the TakeProfit Order. The associated Trade will be
                closed by a market price that is equal to or better than this threshold.
            time_in_force (Union[Unset, TakeProfitOrderTimeInForce]): The time-in-force requested for the TakeProfit Order.
                Restricted to "GTC", "GFD" and "GTD" for TakeProfit Orders.
            gtd_time (Union[Unset, str]): The date/time when the TakeProfit Order will be cancelled if its timeInForce is
                "GTD".
            trigger_condition (Union[Unset, TakeProfitOrderTriggerCondition]): Specification of which price component should
                be used when determining if an Order should be triggered and filled. This allows Orders to be triggered based on
                the bid, ask, mid, default (ask for buy, bid for sell) or inverse (ask for sell, bid for buy) price depending on
                the desired behaviour. Orders are always filled using their default price component.
                This feature is only provided through the REST API. Clients who choose to specify a non-default trigger
                condition will not see it reflected in any of OANDA's proprietary or partner trading platforms, their
                transaction history or their account statements. OANDA platforms always assume that an Order's trigger condition
                is set to the default value when indicating the distance from an Order's trigger price, and will always provide
                the default trigger condition when creating or modifying an Order.
                A special restriction applies when creating a guaranteed Stop Loss Order. In this case the TriggerCondition
                value must either be "DEFAULT", or the "natural" trigger side "DEFAULT" results in. So for a Stop Loss Order for
                a long trade valid values are "DEFAULT" and "BID", and for short trades "DEFAULT" and "ASK" are valid.
            filling_transaction_id (Union[Unset, str]): ID of the Transaction that filled this Order (only provided when the
                Order's state is FILLED)
            filled_time (Union[Unset, str]): Date/time when the Order was filled (only provided when the Order's state is
                FILLED)
            trade_opened_id (Union[Unset, str]): Trade ID of Trade opened when the Order was filled (only provided when the
                Order's state is FILLED and a Trade was opened as a result of the fill)
            trade_reduced_id (Union[Unset, str]): Trade ID of Trade reduced when the Order was filled (only provided when
                the Order's state is FILLED and a Trade was reduced as a result of the fill)
            trade_closed_i_ds (Union[Unset, List[str]]): Trade IDs of Trades closed when the Order was filled (only provided
                when the Order's state is FILLED and one or more Trades were closed as a result of the fill)
            cancelling_transaction_id (Union[Unset, str]): ID of the Transaction that cancelled the Order (only provided
                when the Order's state is CANCELLED)
            cancelled_time (Union[Unset, str]): Date/time when the Order was cancelled (only provided when the state of the
                Order is CANCELLED)
            replaces_order_id (Union[Unset, str]): The ID of the Order that was replaced by this Order (only provided if
                this Order was created as part of a cancel/replace).
            replaced_by_order_id (Union[Unset, str]): The ID of the Order that replaced this Order (only provided if this
                Order was cancelled as part of a cancel/replace).
    """

    id: Union[Unset, str] = UNSET
    create_time: Union[Unset, str] = UNSET
    state: Union[Unset, TakeProfitOrderState] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    type: Union[Unset, TakeProfitOrderType] = UNSET
    trade_id: Union[Unset, str] = UNSET
    client_trade_id: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    time_in_force: Union[Unset, TakeProfitOrderTimeInForce] = UNSET
    gtd_time: Union[Unset, str] = UNSET
    trigger_condition: Union[Unset, TakeProfitOrderTriggerCondition] = UNSET
    filling_transaction_id: Union[Unset, str] = UNSET
    filled_time: Union[Unset, str] = UNSET
    trade_opened_id: Union[Unset, str] = UNSET
    trade_reduced_id: Union[Unset, str] = UNSET
    trade_closed_i_ds: Union[Unset, List[str]] = UNSET
    cancelling_transaction_id: Union[Unset, str] = UNSET
    cancelled_time: Union[Unset, str] = UNSET
    replaces_order_id: Union[Unset, str] = UNSET
    replaced_by_order_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        create_time = self.create_time

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state

        client_extensions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.client_extensions, Unset):
            client_extensions = self.client_extensions.to_dict()

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type

        trade_id = self.trade_id

        client_trade_id = self.client_trade_id

        price = self.price

        time_in_force: Union[Unset, str] = UNSET
        if not isinstance(self.time_in_force, Unset):
            time_in_force = self.time_in_force

        gtd_time = self.gtd_time

        trigger_condition: Union[Unset, str] = UNSET
        if not isinstance(self.trigger_condition, Unset):
            trigger_condition = self.trigger_condition

        filling_transaction_id = self.filling_transaction_id

        filled_time = self.filled_time

        trade_opened_id = self.trade_opened_id

        trade_reduced_id = self.trade_reduced_id

        trade_closed_i_ds: Union[Unset, List[str]] = UNSET
        if not isinstance(self.trade_closed_i_ds, Unset):
            trade_closed_i_ds = self.trade_closed_i_ds

        cancelling_transaction_id = self.cancelling_transaction_id

        cancelled_time = self.cancelled_time

        replaces_order_id = self.replaces_order_id

        replaced_by_order_id = self.replaced_by_order_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if create_time is not UNSET:
            field_dict["createTime"] = create_time
        if state is not UNSET:
            field_dict["state"] = state
        if client_extensions is not UNSET:
            field_dict["clientExtensions"] = client_extensions
        if type is not UNSET:
            field_dict["type"] = type
        if trade_id is not UNSET:
            field_dict["tradeID"] = trade_id
        if client_trade_id is not UNSET:
            field_dict["clientTradeID"] = client_trade_id
        if price is not UNSET:
            field_dict["price"] = price
        if time_in_force is not UNSET:
            field_dict["timeInForce"] = time_in_force
        if gtd_time is not UNSET:
            field_dict["gtdTime"] = gtd_time
        if trigger_condition is not UNSET:
            field_dict["triggerCondition"] = trigger_condition
        if filling_transaction_id is not UNSET:
            field_dict["fillingTransactionID"] = filling_transaction_id
        if filled_time is not UNSET:
            field_dict["filledTime"] = filled_time
        if trade_opened_id is not UNSET:
            field_dict["tradeOpenedID"] = trade_opened_id
        if trade_reduced_id is not UNSET:
            field_dict["tradeReducedID"] = trade_reduced_id
        if trade_closed_i_ds is not UNSET:
            field_dict["tradeClosedIDs"] = trade_closed_i_ds
        if cancelling_transaction_id is not UNSET:
            field_dict["cancellingTransactionID"] = cancelling_transaction_id
        if cancelled_time is not UNSET:
            field_dict["cancelledTime"] = cancelled_time
        if replaces_order_id is not UNSET:
            field_dict["replacesOrderID"] = replaces_order_id
        if replaced_by_order_id is not UNSET:
            field_dict["replacedByOrderID"] = replaced_by_order_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.client_extensions import ClientExtensions

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        create_time = d.pop("createTime", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, TakeProfitOrderState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = check_take_profit_order_state(_state)

        _client_extensions = d.pop("clientExtensions", UNSET)
        client_extensions: Union[Unset, ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = UNSET
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)

        _type = d.pop("type", UNSET)
        type: Union[Unset, TakeProfitOrderType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = check_take_profit_order_type(_type)

        trade_id = d.pop("tradeID", UNSET)

        client_trade_id = d.pop("clientTradeID", UNSET)

        price = d.pop("price", UNSET)

        _time_in_force = d.pop("timeInForce", UNSET)
        time_in_force: Union[Unset, TakeProfitOrderTimeInForce]
        if isinstance(_time_in_force, Unset):
            time_in_force = UNSET
        else:
            time_in_force = check_take_profit_order_time_in_force(_time_in_force)

        gtd_time = d.pop("gtdTime", UNSET)

        _trigger_condition = d.pop("triggerCondition", UNSET)
        trigger_condition: Union[Unset, TakeProfitOrderTriggerCondition]
        if isinstance(_trigger_condition, Unset):
            trigger_condition = UNSET
        else:
            trigger_condition = check_take_profit_order_trigger_condition(
                _trigger_condition
            )

        filling_transaction_id = d.pop("fillingTransactionID", UNSET)

        filled_time = d.pop("filledTime", UNSET)

        trade_opened_id = d.pop("tradeOpenedID", UNSET)

        trade_reduced_id = d.pop("tradeReducedID", UNSET)

        trade_closed_i_ds = cast(List[str], d.pop("tradeClosedIDs", UNSET))

        cancelling_transaction_id = d.pop("cancellingTransactionID", UNSET)

        cancelled_time = d.pop("cancelledTime", UNSET)

        replaces_order_id = d.pop("replacesOrderID", UNSET)

        replaced_by_order_id = d.pop("replacedByOrderID", UNSET)

        take_profit_order = cls(
            id=id,
            create_time=create_time,
            state=state,
            client_extensions=client_extensions,
            type=type,
            trade_id=trade_id,
            client_trade_id=client_trade_id,
            price=price,
            time_in_force=time_in_force,
            gtd_time=gtd_time,
            trigger_condition=trigger_condition,
            filling_transaction_id=filling_transaction_id,
            filled_time=filled_time,
            trade_opened_id=trade_opened_id,
            trade_reduced_id=trade_reduced_id,
            trade_closed_i_ds=trade_closed_i_ds,
            cancelling_transaction_id=cancelling_transaction_id,
            cancelled_time=cancelled_time,
            replaces_order_id=replaces_order_id,
            replaced_by_order_id=replaced_by_order_id,
        )

        take_profit_order.additional_properties = d
        return take_profit_order

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
