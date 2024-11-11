from __future__ import annotations
from typing import Dict, Any
import dataclasses
from dacite import from_dict
from .client_price import ClientPrice
from .pricing_heartbeat import PricingHeartbeat
from typing import Optional, TypeVar

T = TypeVar("T", bound="StreamPricingResponse200")


@dataclasses.dataclass
class StreamPricingResponse200:
    """The response body for the Pricing Stream uses chunked transfer encoding.  Each chunk contains Price and/or
    PricingHeartbeat objects encoded as JSON.  Each JSON object is serialized into a single line of text, and multiple
    objects found in the same chunk are separated by newlines.
    Heartbeats are sent every 5 seconds.

        Attributes:
            price (Union[Unset, ClientPrice]): The specification of an Account-specific Price.
            heartbeat (Union[Unset, PricingHeartbeat]): A PricingHeartbeat object is injected into the Pricing stream to
                ensure that the HTTP connection remains active."""

    price: Optional["ClientPrice"]
    heartbeat: Optional["PricingHeartbeat"]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StreamPricingResponse200":
        """Create a new instance from a dictionary."""
        return from_dict(data_class=cls, data=data)
