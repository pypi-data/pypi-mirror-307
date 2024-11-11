from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from typing import Optional, TypeVar

T = TypeVar("T", bound="ConfigureAccountBody")


@dataclasses.dataclass
class ConfigureAccountBody:
    """Attributes:
    alias (Union[Unset, str]): Client-defined alias (name) for the Account
    margin_rate (Union[Unset, str]): The string representation of a decimal number."""

    alias: Optional[str]
    margin_rate: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConfigureAccountBody":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
