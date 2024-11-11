from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="CalculatedAccountState")


@_attrs_define
class CalculatedAccountState:
    """The dynamically calculated state of a client's Account.

    Attributes:
        unrealized_pl (Union[Unset, str]): The total unrealized profit/loss for all Trades currently open in the
            Account.
        nav (Union[Unset, str]): The net asset value of the Account. Equal to Account balance + unrealizedPL.
        margin_used (Union[Unset, str]): Margin currently used for the Account.
        margin_available (Union[Unset, str]): Margin available for Account currency.
        position_value (Union[Unset, str]): The value of the Account's open positions represented in the Account's home
            currency.
        margin_closeout_unrealized_pl (Union[Unset, str]): The Account's margin closeout unrealized PL.
        margin_closeout_nav (Union[Unset, str]): The Account's margin closeout NAV.
        margin_closeout_margin_used (Union[Unset, str]): The Account's margin closeout margin used.
        margin_closeout_percent (Union[Unset, str]): The Account's margin closeout percentage. When this value is 1.0 or
            above the Account is in a margin closeout situation.
        margin_closeout_position_value (Union[Unset, str]): The value of the Account's open positions as used for margin
            closeout calculations represented in the Account's home currency.
        withdrawal_limit (Union[Unset, str]): The current WithdrawalLimit for the account which will be zero or a
            positive value indicating how much can be withdrawn from the account.
        margin_call_margin_used (Union[Unset, str]): The Account's margin call margin used.
        margin_call_percent (Union[Unset, str]): The Account's margin call percentage. When this value is 1.0 or above
            the Account is in a margin call situation.
    """

    unrealized_pl: Union[Unset, str] = UNSET
    nav: Union[Unset, str] = UNSET
    margin_used: Union[Unset, str] = UNSET
    margin_available: Union[Unset, str] = UNSET
    position_value: Union[Unset, str] = UNSET
    margin_closeout_unrealized_pl: Union[Unset, str] = UNSET
    margin_closeout_nav: Union[Unset, str] = UNSET
    margin_closeout_margin_used: Union[Unset, str] = UNSET
    margin_closeout_percent: Union[Unset, str] = UNSET
    margin_closeout_position_value: Union[Unset, str] = UNSET
    withdrawal_limit: Union[Unset, str] = UNSET
    margin_call_margin_used: Union[Unset, str] = UNSET
    margin_call_percent: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        unrealized_pl = self.unrealized_pl

        nav = self.nav

        margin_used = self.margin_used

        margin_available = self.margin_available

        position_value = self.position_value

        margin_closeout_unrealized_pl = self.margin_closeout_unrealized_pl

        margin_closeout_nav = self.margin_closeout_nav

        margin_closeout_margin_used = self.margin_closeout_margin_used

        margin_closeout_percent = self.margin_closeout_percent

        margin_closeout_position_value = self.margin_closeout_position_value

        withdrawal_limit = self.withdrawal_limit

        margin_call_margin_used = self.margin_call_margin_used

        margin_call_percent = self.margin_call_percent

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if unrealized_pl is not UNSET:
            field_dict["unrealizedPL"] = unrealized_pl
        if nav is not UNSET:
            field_dict["NAV"] = nav
        if margin_used is not UNSET:
            field_dict["marginUsed"] = margin_used
        if margin_available is not UNSET:
            field_dict["marginAvailable"] = margin_available
        if position_value is not UNSET:
            field_dict["positionValue"] = position_value
        if margin_closeout_unrealized_pl is not UNSET:
            field_dict["marginCloseoutUnrealizedPL"] = margin_closeout_unrealized_pl
        if margin_closeout_nav is not UNSET:
            field_dict["marginCloseoutNAV"] = margin_closeout_nav
        if margin_closeout_margin_used is not UNSET:
            field_dict["marginCloseoutMarginUsed"] = margin_closeout_margin_used
        if margin_closeout_percent is not UNSET:
            field_dict["marginCloseoutPercent"] = margin_closeout_percent
        if margin_closeout_position_value is not UNSET:
            field_dict["marginCloseoutPositionValue"] = margin_closeout_position_value
        if withdrawal_limit is not UNSET:
            field_dict["withdrawalLimit"] = withdrawal_limit
        if margin_call_margin_used is not UNSET:
            field_dict["marginCallMarginUsed"] = margin_call_margin_used
        if margin_call_percent is not UNSET:
            field_dict["marginCallPercent"] = margin_call_percent

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        unrealized_pl = d.pop("unrealizedPL", UNSET)

        nav = d.pop("NAV", UNSET)

        margin_used = d.pop("marginUsed", UNSET)

        margin_available = d.pop("marginAvailable", UNSET)

        position_value = d.pop("positionValue", UNSET)

        margin_closeout_unrealized_pl = d.pop("marginCloseoutUnrealizedPL", UNSET)

        margin_closeout_nav = d.pop("marginCloseoutNAV", UNSET)

        margin_closeout_margin_used = d.pop("marginCloseoutMarginUsed", UNSET)

        margin_closeout_percent = d.pop("marginCloseoutPercent", UNSET)

        margin_closeout_position_value = d.pop("marginCloseoutPositionValue", UNSET)

        withdrawal_limit = d.pop("withdrawalLimit", UNSET)

        margin_call_margin_used = d.pop("marginCallMarginUsed", UNSET)

        margin_call_percent = d.pop("marginCallPercent", UNSET)

        calculated_account_state = cls(
            unrealized_pl=unrealized_pl,
            nav=nav,
            margin_used=margin_used,
            margin_available=margin_available,
            position_value=position_value,
            margin_closeout_unrealized_pl=margin_closeout_unrealized_pl,
            margin_closeout_nav=margin_closeout_nav,
            margin_closeout_margin_used=margin_closeout_margin_used,
            margin_closeout_percent=margin_closeout_percent,
            margin_closeout_position_value=margin_closeout_position_value,
            withdrawal_limit=withdrawal_limit,
            margin_call_margin_used=margin_call_margin_used,
            margin_call_percent=margin_call_percent,
        )

        calculated_account_state.additional_properties = d
        return calculated_account_state

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
