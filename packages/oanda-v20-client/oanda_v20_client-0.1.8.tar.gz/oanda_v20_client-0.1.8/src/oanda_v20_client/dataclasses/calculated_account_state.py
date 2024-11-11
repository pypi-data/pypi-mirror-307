from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="CalculatedAccountState")


@dataclasses.dataclass
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
            the Account is in a margin call situation."""

    unrealized_pl: Optional[str]
    nav: Optional[str]
    margin_used: Optional[str]
    margin_available: Optional[str]
    position_value: Optional[str]
    margin_closeout_unrealized_pl: Optional[str]
    margin_closeout_nav: Optional[str]
    margin_closeout_margin_used: Optional[str]
    margin_closeout_percent: Optional[str]
    margin_closeout_position_value: Optional[str]
    withdrawal_limit: Optional[str]
    margin_call_margin_used: Optional[str]
    margin_call_percent: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        unrealized_pl = d.pop("unrealizedPL", None)
        nav = d.pop("NAV", None)
        margin_used = d.pop("marginUsed", None)
        margin_available = d.pop("marginAvailable", None)
        position_value = d.pop("positionValue", None)
        margin_closeout_unrealized_pl = d.pop("marginCloseoutUnrealizedPL", None)
        margin_closeout_nav = d.pop("marginCloseoutNAV", None)
        margin_closeout_margin_used = d.pop("marginCloseoutMarginUsed", None)
        margin_closeout_percent = d.pop("marginCloseoutPercent", None)
        margin_closeout_position_value = d.pop("marginCloseoutPositionValue", None)
        withdrawal_limit = d.pop("withdrawalLimit", None)
        margin_call_margin_used = d.pop("marginCallMarginUsed", None)
        margin_call_percent = d.pop("marginCallPercent", None)
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

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
