from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="ConfigureAccountBody")


@dataclasses.dataclass
class ConfigureAccountBody:
    """Attributes:
    alias (Union[Unset, str]): Client-defined alias (name) for the Account
    margin_rate (Union[Unset, str]): The string representation of a decimal number."""

    alias: Optional[str]
    margin_rate: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        alias = d.pop("alias", None)
        margin_rate = d.pop("marginRate", None)
        configure_account_body = cls(alias=alias, margin_rate=margin_rate)
        configure_account_body.additional_properties = d
        return configure_account_body

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
