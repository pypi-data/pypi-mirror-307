from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.market_order_margin_closeout_reason import (
    check_market_order_margin_closeout_reason,
)
from ..models.market_order_margin_closeout_reason import MarketOrderMarginCloseoutReason
from typing import Union


T = TypeVar("T", bound="MarketOrderMarginCloseout")


@_attrs_define
class MarketOrderMarginCloseout:
    """Details for the Market Order extensions specific to a Market Order placed that is part of a Market Order Margin
    Closeout in a client's account

        Attributes:
            reason (Union[Unset, MarketOrderMarginCloseoutReason]): The reason the Market Order was created to perform a
                margin closeout
    """

    reason: Union[Unset, MarketOrderMarginCloseoutReason] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        reason: Union[Unset, str] = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _reason = d.pop("reason", UNSET)
        reason: Union[Unset, MarketOrderMarginCloseoutReason]
        if isinstance(_reason, Unset):
            reason = UNSET
        else:
            reason = check_market_order_margin_closeout_reason(_reason)

        market_order_margin_closeout = cls(
            reason=reason,
        )

        market_order_margin_closeout.additional_properties = d
        return market_order_margin_closeout

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
