from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from typing import Optional, TypeVar

T = TypeVar("T", bound="QuoteHomeConversionFactors")


@dataclasses.dataclass
class QuoteHomeConversionFactors:
    """QuoteHomeConversionFactors represents the factors that can be used used to convert quantities of a Price's
    Instrument's quote currency into the Account's home currency.

        Attributes:
            positive_units (Union[Unset, str]): The factor used to convert a positive amount of the Price's Instrument's
                quote currency into a positive amount of the Account's home currency.  Conversion is performed by multiplying
                the quote units by the conversion factor.
            negative_units (Union[Unset, str]): The factor used to convert a negative amount of the Price's Instrument's
                quote currency into a negative amount of the Account's home currency.  Conversion is performed by multiplying
                the quote units by the conversion factor."""

    positive_units: Optional[str]
    negative_units: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QuoteHomeConversionFactors":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
