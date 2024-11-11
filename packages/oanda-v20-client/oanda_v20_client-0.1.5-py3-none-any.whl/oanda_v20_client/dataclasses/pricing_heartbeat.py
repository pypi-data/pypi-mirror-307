from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from ..types import UNSET, Unset
from typing import TypeVar, Union

T = TypeVar("T", bound="PricingHeartbeat")


@dataclasses.dataclass
class PricingHeartbeat:
    """A PricingHeartbeat object is injected into the Pricing stream to ensure that the HTTP connection remains active.

    Attributes:
        type (Union[Unset, str]): The string "HEARTBEAT"
        time (Union[Unset, str]): The date/time when the Heartbeat was created."""

    type: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PricingHeartbeat":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
