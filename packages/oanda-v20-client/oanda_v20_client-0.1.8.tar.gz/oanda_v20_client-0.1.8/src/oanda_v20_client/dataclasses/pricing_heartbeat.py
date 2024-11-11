from __future__ import annotations
from typing import Dict, Any
import dataclasses
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="PricingHeartbeat")


@dataclasses.dataclass
class PricingHeartbeat:
    """A PricingHeartbeat object is injected into the Pricing stream to ensure that the HTTP connection remains active.

    Attributes:
        type (Union[Unset, str]): The string "HEARTBEAT"
        time (Union[Unset, str]): The date/time when the Heartbeat was created."""

    type: Optional[str]
    time: Optional[str]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type", None)
        time = d.pop("time", None)
        pricing_heartbeat = cls(type=type, time=time)
        pricing_heartbeat.additional_properties = d
        return pricing_heartbeat

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
