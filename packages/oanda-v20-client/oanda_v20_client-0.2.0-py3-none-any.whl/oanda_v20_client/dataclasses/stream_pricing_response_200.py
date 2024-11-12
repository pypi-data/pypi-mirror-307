from __future__ import annotations
from typing import Dict, Any
import dataclasses
from .client_price import ClientPrice
from .pricing_heartbeat import PricingHeartbeat
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound="StreamPricingResponse200")


@dataclasses.dataclass
class StreamPricingResponse200:
    """The response body for the Pricing Stream uses chunked transfer encoding.  Each chunk contains Price and/or
    PricingHeartbeat objects encoded as JSON.  Each JSON object is serialized into a single line of text, and multiple
    objects found in the same chunk are separated by newlines.
    Heartbeats are sent every 5 seconds.

        Attributes:
            price (Optional[ClientPrice]): The specification of an Account-specific Price.
            heartbeat (Optional[PricingHeartbeat]): A PricingHeartbeat object is injected into the Pricing stream to
                ensure that the HTTP connection remains active."""

    price: Optional["ClientPrice"]
    heartbeat: Optional["PricingHeartbeat"]

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from .pricing_heartbeat import PricingHeartbeat
        from .client_price import ClientPrice

        d = src_dict.copy()
        _price = d.pop("price", None)
        price: Optional[ClientPrice]
        if _price is None:
            price = None
        else:
            price = ClientPrice.from_dict(_price)
        _heartbeat = d.pop("heartbeat", None)
        heartbeat: Optional[PricingHeartbeat]
        if _heartbeat is None:
            heartbeat = None
        else:
            heartbeat = PricingHeartbeat.from_dict(_heartbeat)
        stream_pricing_response_200 = cls(price=price, heartbeat=heartbeat)
        return stream_pricing_response_200

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass instance to a dictionary."""
        return dataclasses.asdict(self)
