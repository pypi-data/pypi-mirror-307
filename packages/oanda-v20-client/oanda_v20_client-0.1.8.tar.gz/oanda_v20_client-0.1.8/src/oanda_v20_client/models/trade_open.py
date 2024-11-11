from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.client_extensions import ClientExtensions


T = TypeVar("T", bound="TradeOpen")


@_attrs_define
class TradeOpen:
    """A TradeOpen object represents a Trade for an instrument that was opened in an Account. It is found embedded in
    Transactions that affect the position of an instrument in the Account, specifically the OrderFill Transaction.

        Attributes:
            trade_id (Union[Unset, str]): The ID of the Trade that was opened
            units (Union[Unset, str]): The number of units opened by the Trade
            price (Union[Unset, str]): The average price that the units were opened at.
            guaranteed_execution_fee (Union[Unset, str]): This is the fee charged for opening the trade if it has a
                guaranteed Stop Loss Order attached to it.
            client_extensions (Union[Unset, ClientExtensions]): A ClientExtensions object allows a client to attach a
                clientID, tag and comment to Orders and Trades in their Account.  Do not set, modify, or delete this field if
                your account is associated with MT4.
            half_spread_cost (Union[Unset, str]): The half spread cost for the trade open. This can be a positive or
                negative value and is represented in the home currency of the Account.
            initial_margin_required (Union[Unset, str]): The margin required at the time the Trade was created. Note, this
                is the 'pure' margin required, it is not the 'effective' margin used that factors in the trade risk if a GSLO is
                attached to the trade.
    """

    trade_id: Union[Unset, str] = UNSET
    units: Union[Unset, str] = UNSET
    price: Union[Unset, str] = UNSET
    guaranteed_execution_fee: Union[Unset, str] = UNSET
    client_extensions: Union[Unset, "ClientExtensions"] = UNSET
    half_spread_cost: Union[Unset, str] = UNSET
    initial_margin_required: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trade_id = self.trade_id

        units = self.units

        price = self.price

        guaranteed_execution_fee = self.guaranteed_execution_fee

        client_extensions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.client_extensions, Unset):
            client_extensions = self.client_extensions.to_dict()

        half_spread_cost = self.half_spread_cost

        initial_margin_required = self.initial_margin_required

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if trade_id is not UNSET:
            field_dict["tradeID"] = trade_id
        if units is not UNSET:
            field_dict["units"] = units
        if price is not UNSET:
            field_dict["price"] = price
        if guaranteed_execution_fee is not UNSET:
            field_dict["guaranteedExecutionFee"] = guaranteed_execution_fee
        if client_extensions is not UNSET:
            field_dict["clientExtensions"] = client_extensions
        if half_spread_cost is not UNSET:
            field_dict["halfSpreadCost"] = half_spread_cost
        if initial_margin_required is not UNSET:
            field_dict["initialMarginRequired"] = initial_margin_required

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.client_extensions import ClientExtensions

        d = src_dict.copy()
        trade_id = d.pop("tradeID", UNSET)

        units = d.pop("units", UNSET)

        price = d.pop("price", UNSET)

        guaranteed_execution_fee = d.pop("guaranteedExecutionFee", UNSET)

        _client_extensions = d.pop("clientExtensions", UNSET)
        client_extensions: Union[Unset, ClientExtensions]
        if isinstance(_client_extensions, Unset):
            client_extensions = UNSET
        else:
            client_extensions = ClientExtensions.from_dict(_client_extensions)

        half_spread_cost = d.pop("halfSpreadCost", UNSET)

        initial_margin_required = d.pop("initialMarginRequired", UNSET)

        trade_open = cls(
            trade_id=trade_id,
            units=units,
            price=price,
            guaranteed_execution_fee=guaranteed_execution_fee,
            client_extensions=client_extensions,
            half_spread_cost=half_spread_cost,
            initial_margin_required=initial_margin_required,
        )

        trade_open.additional_properties = d
        return trade_open

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
