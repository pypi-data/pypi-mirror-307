from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="OpenTradeFinancing")


@_attrs_define
class OpenTradeFinancing:
    """OpenTradeFinancing is used to pay/collect daily financing charge for an open Trade within an Account

    Attributes:
        trade_id (Union[Unset, str]): The ID of the Trade that financing is being paid/collected for.
        financing (Union[Unset, str]): The amount of financing paid/collected for the Trade.
    """

    trade_id: Union[Unset, str] = UNSET
    financing: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trade_id = self.trade_id

        financing = self.financing

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if trade_id is not UNSET:
            field_dict["tradeID"] = trade_id
        if financing is not UNSET:
            field_dict["financing"] = financing

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trade_id = d.pop("tradeID", UNSET)

        financing = d.pop("financing", UNSET)

        open_trade_financing = cls(
            trade_id=trade_id,
            financing=financing,
        )

        open_trade_financing.additional_properties = d
        return open_trade_financing

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
