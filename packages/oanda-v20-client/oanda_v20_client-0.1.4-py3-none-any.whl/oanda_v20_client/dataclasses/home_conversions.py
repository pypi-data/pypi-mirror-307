from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from typing import TypeVar, Union

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

    currency: Union[Unset, str] = UNSET
    account_gain: Union[Unset, str] = UNSET
    account_loss: Union[Unset, str] = UNSET
    position_value: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HomeConversions":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
