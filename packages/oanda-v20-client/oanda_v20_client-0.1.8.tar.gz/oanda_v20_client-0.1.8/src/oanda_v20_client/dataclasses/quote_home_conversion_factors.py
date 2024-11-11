from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

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

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        positive_units = d.pop("positiveUnits", None)
        negative_units = d.pop("negativeUnits", None)
        quote_home_conversion_factors = cls(
            positive_units=positive_units, negative_units=negative_units
        )
        quote_home_conversion_factors.additional_properties = d
        return quote_home_conversion_factors

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
