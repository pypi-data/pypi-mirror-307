from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.order_fill_transaction_reason import check_order_fill_transaction_reason
from ..models.order_fill_transaction_reason import OrderFillTransactionReason
from ..models.order_fill_transaction_type import check_order_fill_transaction_type
from ..models.order_fill_transaction_type import OrderFillTransactionType
from typing import Union

if TYPE_CHECKING:
    from ..models.client_price import ClientPrice
    from ..models.trade_open import TradeOpen
    from ..models.trade_reduce import TradeReduce


T = TypeVar("T", bound="OrderFillTransaction")


@_attrs_define
class OrderFillTransaction:
    """An OrderFillTransaction represents the filling of an Order in the client's Account.

    Attributes:
        id (Union[Unset, str]): The Transaction's Identifier.
        time (Union[Unset, str]): The date/time when the Transaction was created.
        user_id (Union[Unset, int]): The ID of the user that initiated the creation of the Transaction.
        account_id (Union[Unset, str]): The ID of the Account the Transaction was created for.
        batch_id (Union[Unset, str]): The ID of the "batch" that the Transaction belongs to. Transactions in the same
            batch are applied to the Account simultaneously.
        request_id (Union[Unset, str]): The Request ID of the request which generated the transaction.
        type (Union[Unset, OrderFillTransactionType]): The Type of the Transaction. Always set to "ORDER_FILL" for an
            OrderFillTransaction.
        order_id (Union[Unset, str]): The ID of the Order filled.
        client_order_id (Union[Unset, str]): The client Order ID of the Order filled (only provided if the client has
            assigned one).
        instrument (Union[Unset, str]): The name of the filled Order's instrument.
        units (Union[Unset, str]): The number of units filled by the OrderFill.
        gain_quote_home_conversion_factor (Union[Unset, str]): This is the conversion factor in effect for the Account
            at the time of the OrderFill for converting any gains realized in Instrument quote units into units of the
            Account's home currency.
        loss_quote_home_conversion_factor (Union[Unset, str]): This is the conversion factor in effect for the Account
            at the time of the OrderFill for converting any losses realized in Instrument quote units into units of the
            Account's home currency.
        price (Union[Unset, str]): This field is now deprecated and should no longer be used. The individual
            tradesClosed, tradeReduced and tradeOpened fields contain the exact/official price each unit was filled at.
        full_vwap (Union[Unset, str]): The price that all of the units of the OrderFill should have been filled at, in
            the absence of guaranteed price execution. This factors in the Account's current ClientPrice, used liquidity and
            the units of the OrderFill only. If no Trades were closed with their price clamped for guaranteed stop loss
            enforcement, then this value will match the price fields of each Trade opened, closed, and reduced, and they
            will all be the exact same.
        full_price (Union[Unset, ClientPrice]): The specification of an Account-specific Price.
        reason (Union[Unset, OrderFillTransactionReason]): The reason that an Order was filled
        pl (Union[Unset, str]): The profit or loss incurred when the Order was filled.
        financing (Union[Unset, str]): The financing paid or collected when the Order was filled.
        commission (Union[Unset, str]): The commission charged in the Account's home currency as a result of filling the
            Order. The commission is always represented as a positive quantity of the Account's home currency, however it
            reduces the balance in the Account.
        guaranteed_execution_fee (Union[Unset, str]): The total guaranteed execution fees charged for all Trades opened,
            closed or reduced with guaranteed Stop Loss Orders.
        account_balance (Union[Unset, str]): The Account's balance after the Order was filled.
        trade_opened (Union[Unset, TradeOpen]): A TradeOpen object represents a Trade for an instrument that was opened
            in an Account. It is found embedded in Transactions that affect the position of an instrument in the Account,
            specifically the OrderFill Transaction.
        trades_closed (Union[Unset, List['TradeReduce']]): The Trades that were closed when the Order was filled (only
            provided if filling the Order resulted in a closing open Trades).
        trade_reduced (Union[Unset, TradeReduce]): A TradeReduce object represents a Trade for an instrument that was
            reduced (either partially or fully) in an Account. It is found embedded in Transactions that affect the position
            of an instrument in the account, specifically the OrderFill Transaction.
        half_spread_cost (Union[Unset, str]): The half spread cost for the OrderFill, which is the sum of the
            halfSpreadCost values in the tradeOpened, tradesClosed and tradeReduced fields. This can be a positive or
            negative value and is represented in the home currency of the Account.
    """

    id: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    account_id: Union[Unset, str] = UNSET
    batch_id: Union[Unset, str] = UNSET
    request_id: Union[Unset, str] = UNSET
    type: Union[Unset, OrderFillTransactionType] = UNSET
    order_id: Union[Unset, str] = UNSET
    client_order_id: Union[Unset, str] = UNSET
    instrument: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET
    gain_quote_home_conversion_factor: Union[Unset, str] = UNSET
    loss_quote_home_conversion_factor: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    full_vwap: Union[Unset, str] = UNSET
    full_price: Union[Unset, "ClientPrice"] = UNSET
    reason: Union[Unset, OrderFillTransactionReason] = UNSET
    pl: Union[Unset, str] = UNSET
    financing: Union[Unset, str] = UNSET
    commission: Union[Unset, str] = UNSET
    guaranteed_execution_fee: Union[Unset, str] = UNSET
    account_balance: Union[Unset, str] = UNSET
    trade_opened: Union[Unset, "TradeOpen"] = UNSET
    trades_closed: Union[Unset, List["TradeReduce"]] = UNSET
    trade_reduced: Union[Unset, "TradeReduce"] = UNSET
    half_spread_cost: Union[Unset, str] = UNSET
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

        order_id = self.order_id

        client_order_id = self.client_order_id

        instrument = self.instrument

        units = self.units

        gain_quote_home_conversion_factor = self.gain_quote_home_conversion_factor

        loss_quote_home_conversion_factor = self.loss_quote_home_conversion_factor

        price = self.price

        full_vwap = self.full_vwap

        full_price: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.full_price, Unset):
            full_price = self.full_price.to_dict()

        reason: Union[Unset, str] = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason

        pl = self.pl

        financing = self.financing

        commission = self.commission

        guaranteed_execution_fee = self.guaranteed_execution_fee

        account_balance = self.account_balance

        trade_opened: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.trade_opened, Unset):
            trade_opened = self.trade_opened.to_dict()

        trades_closed: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.trades_closed, Unset):
            trades_closed = []
            for trades_closed_item_data in self.trades_closed:
                trades_closed_item = trades_closed_item_data.to_dict()
                trades_closed.append(trades_closed_item)

        trade_reduced: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.trade_reduced, Unset):
            trade_reduced = self.trade_reduced.to_dict()

        half_spread_cost = self.half_spread_cost

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
        if order_id is not UNSET:
            field_dict["orderID"] = order_id
        if client_order_id is not UNSET:
            field_dict["clientOrderID"] = client_order_id
        if instrument is not UNSET:
            field_dict["instrument"] = instrument
        if units is not UNSET:
            field_dict["units"] = units
        if gain_quote_home_conversion_factor is not UNSET:
            field_dict["gainQuoteHomeConversionFactor"] = (
                gain_quote_home_conversion_factor
            )
        if loss_quote_home_conversion_factor is not UNSET:
            field_dict["lossQuoteHomeConversionFactor"] = (
                loss_quote_home_conversion_factor
            )
        if price is not UNSET:
            field_dict["price"] = price
        if full_vwap is not UNSET:
            field_dict["fullVWAP"] = full_vwap
        if full_price is not UNSET:
            field_dict["fullPrice"] = full_price
        if reason is not UNSET:
            field_dict["reason"] = reason
        if pl is not UNSET:
            field_dict["pl"] = pl
        if financing is not UNSET:
            field_dict["financing"] = financing
        if commission is not UNSET:
            field_dict["commission"] = commission
        if guaranteed_execution_fee is not UNSET:
            field_dict["guaranteedExecutionFee"] = guaranteed_execution_fee
        if account_balance is not UNSET:
            field_dict["accountBalance"] = account_balance
        if trade_opened is not UNSET:
            field_dict["tradeOpened"] = trade_opened
        if trades_closed is not UNSET:
            field_dict["tradesClosed"] = trades_closed
        if trade_reduced is not UNSET:
            field_dict["tradeReduced"] = trade_reduced
        if half_spread_cost is not UNSET:
            field_dict["halfSpreadCost"] = half_spread_cost

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.client_price import ClientPrice
        from ..models.trade_open import TradeOpen
        from ..models.trade_reduce import TradeReduce

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        time = d.pop("time", UNSET)

        user_id = d.pop("userID", UNSET)

        account_id = d.pop("accountID", UNSET)

        batch_id = d.pop("batchID", UNSET)

        request_id = d.pop("requestID", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, OrderFillTransactionType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = check_order_fill_transaction_type(_type)

        order_id = d.pop("orderID", UNSET)

        client_order_id = d.pop("clientOrderID", UNSET)

        instrument = d.pop("instrument", UNSET)

        units = d.pop("units", UNSET)

        gain_quote_home_conversion_factor = d.pop(
            "gainQuoteHomeConversionFactor", UNSET
        )

        loss_quote_home_conversion_factor = d.pop(
            "lossQuoteHomeConversionFactor", UNSET
        )

        price = d.pop("price", UNSET)

        full_vwap = d.pop("fullVWAP", UNSET)

        _full_price = d.pop("fullPrice", UNSET)
        full_price: Union[Unset, ClientPrice]
        if isinstance(_full_price, Unset):
            full_price = UNSET
        else:
            full_price = ClientPrice.from_dict(_full_price)

        _reason = d.pop("reason", UNSET)
        reason: Union[Unset, OrderFillTransactionReason]
        if isinstance(_reason, Unset):
            reason = UNSET
        else:
            reason = check_order_fill_transaction_reason(_reason)

        pl = d.pop("pl", UNSET)

        financing = d.pop("financing", UNSET)

        commission = d.pop("commission", UNSET)

        guaranteed_execution_fee = d.pop("guaranteedExecutionFee", UNSET)

        account_balance = d.pop("accountBalance", UNSET)

        _trade_opened = d.pop("tradeOpened", UNSET)
        trade_opened: Union[Unset, TradeOpen]
        if isinstance(_trade_opened, Unset):
            trade_opened = UNSET
        else:
            trade_opened = TradeOpen.from_dict(_trade_opened)

        trades_closed = []
        _trades_closed = d.pop("tradesClosed", UNSET)
        for trades_closed_item_data in _trades_closed or []:
            trades_closed_item = TradeReduce.from_dict(trades_closed_item_data)

            trades_closed.append(trades_closed_item)

        _trade_reduced = d.pop("tradeReduced", UNSET)
        trade_reduced: Union[Unset, TradeReduce]
        if isinstance(_trade_reduced, Unset):
            trade_reduced = UNSET
        else:
            trade_reduced = TradeReduce.from_dict(_trade_reduced)

        half_spread_cost = d.pop("halfSpreadCost", UNSET)

        order_fill_transaction = cls(
            id=id,
            time=time,
            user_id=user_id,
            account_id=account_id,
            batch_id=batch_id,
            request_id=request_id,
            type=type,
            order_id=order_id,
            client_order_id=client_order_id,
            instrument=instrument,
            units=units,
            gain_quote_home_conversion_factor=gain_quote_home_conversion_factor,
            loss_quote_home_conversion_factor=loss_quote_home_conversion_factor,
            price=price,
            full_vwap=full_vwap,
            full_price=full_price,
            reason=reason,
            pl=pl,
            financing=financing,
            commission=commission,
            guaranteed_execution_fee=guaranteed_execution_fee,
            account_balance=account_balance,
            trade_opened=trade_opened,
            trades_closed=trades_closed,
            trade_reduced=trade_reduced,
            half_spread_cost=half_spread_cost,
        )

        order_fill_transaction.additional_properties = d
        return order_fill_transaction

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
