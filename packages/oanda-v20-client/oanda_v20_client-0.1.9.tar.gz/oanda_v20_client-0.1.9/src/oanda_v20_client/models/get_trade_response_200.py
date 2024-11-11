from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.trade import Trade


T = TypeVar("T", bound="GetTradeResponse200")


@_attrs_define
class GetTradeResponse200:
    """
    Attributes:
        trade (Union[Unset, Trade]): The specification of a Trade within an Account. This includes the full
            representation of the Trade's dependent Orders in addition to the IDs of those Orders.
        last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account
    """

    trade: Union[Unset, "Trade"] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trade: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.trade, Unset):
            trade = self.trade.to_dict()

        last_transaction_id = self.last_transaction_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if trade is not UNSET:
            field_dict["trade"] = trade
        if last_transaction_id is not UNSET:
            field_dict["lastTransactionID"] = last_transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.trade import Trade

        d = src_dict.copy()
        _trade = d.pop("trade", UNSET)
        trade: Union[Unset, Trade]
        if isinstance(_trade, Unset):
            trade = UNSET
        else:
            trade = Trade.from_dict(_trade)

        last_transaction_id = d.pop("lastTransactionID", UNSET)

        get_trade_response_200 = cls(
            trade=trade,
            last_transaction_id=last_transaction_id,
        )

        get_trade_response_200.additional_properties = d
        return get_trade_response_200

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
