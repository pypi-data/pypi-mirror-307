from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="HomeConversions")


@dataclasses.dataclass
class HomeConversions:
    """HomeConversions represents the factors to use to convert quantities of a given currency into the Account's home
    currency. The conversion factor depends on the scenario the conversion is required for.

        Attributes:
            currency (Union[Unset, str]): The currency to be converted into the home currency.
            account_gain (Union[Unset, str]): The factor used to convert any gains for an Account in the specified currency
                into the Account's home currency. This would include positive realized P/L and positive financing amounts.
                Conversion is performed by multiplying the positive P/L by the conversion factor.
            account_loss (Union[Unset, str]): The string representation of a decimal number.
            position_value (Union[Unset, str]): The factor used to convert a Position or Trade Value in the specified
                currency into the Account's home currency. Conversion is performed by multiplying the Position or Trade Value by
                the conversion factor."""

    currency: Optional[str]
    account_gain: Optional[str]
    account_loss: Optional[str]
    position_value: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        currency = d.pop("currency", None)
        account_gain = d.pop("accountGain", None)
        account_loss = d.pop("accountLoss", None)
        position_value = d.pop("positionValue", None)
        home_conversions = cls(
            currency=currency,
            account_gain=account_gain,
            account_loss=account_loss,
            position_value=position_value,
        )
        home_conversions.additional_properties = d
        return home_conversions

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
