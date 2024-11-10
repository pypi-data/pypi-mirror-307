from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="CalculatedTradeState")


@_attrs_define
class CalculatedTradeState:
    """The dynamic (calculated) state of an open Trade

    Attributes:
        id (Union[Unset, str]): The Trade's ID.
        unrealized_pl (Union[Unset, str]): The Trade's unrealized profit/loss.
        margin_used (Union[Unset, str]): Margin currently used by the Trade.
    """

    id: Union[Unset, str] = UNSET
    unrealized_pl: Union[Unset, str] = UNSET
    margin_used: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        unrealized_pl = self.unrealized_pl

        margin_used = self.margin_used

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if unrealized_pl is not UNSET:
            field_dict["unrealizedPL"] = unrealized_pl
        if margin_used is not UNSET:
            field_dict["marginUsed"] = margin_used

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        unrealized_pl = d.pop("unrealizedPL", UNSET)

        margin_used = d.pop("marginUsed", UNSET)

        calculated_trade_state = cls(
            id=id,
            unrealized_pl=unrealized_pl,
            margin_used=margin_used,
        )

        calculated_trade_state.additional_properties = d
        return calculated_trade_state

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
