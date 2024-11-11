from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.trade import Trade


T = TypeVar("T", bound="ListTradesResponse200")


@_attrs_define
class ListTradesResponse200:
    """
    Attributes:
        trades (Union[Unset, List['Trade']]): The list of Trade detail objects
        last_transaction_id (Union[Unset, str]): The ID of the most recent Transaction created for the Account
    """

    trades: Union[Unset, List["Trade"]] = UNSET
    last_transaction_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trades: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.trades, Unset):
            trades = []
            for trades_item_data in self.trades:
                trades_item = trades_item_data.to_dict()
                trades.append(trades_item)

        last_transaction_id = self.last_transaction_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if trades is not UNSET:
            field_dict["trades"] = trades
        if last_transaction_id is not UNSET:
            field_dict["lastTransactionID"] = last_transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.trade import Trade

        d = src_dict.copy()
        trades = []
        _trades = d.pop("trades", UNSET)
        for trades_item_data in _trades or []:
            trades_item = Trade.from_dict(trades_item_data)

            trades.append(trades_item)

        last_transaction_id = d.pop("lastTransactionID", UNSET)

        list_trades_response_200 = cls(
            trades=trades,
            last_transaction_id=last_transaction_id,
        )

        list_trades_response_200.additional_properties = d
        return list_trades_response_200

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
