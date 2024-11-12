from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.pricing_heartbeat import PricingHeartbeat
    from ..models.client_price import ClientPrice


T = TypeVar("T", bound="StreamPricingResponse200")


@_attrs_define
class StreamPricingResponse200:
    """The response body for the Pricing Stream uses chunked transfer encoding.  Each chunk contains Price and/or
    PricingHeartbeat objects encoded as JSON.  Each JSON object is serialized into a single line of text, and multiple
    objects found in the same chunk are separated by newlines.
    Heartbeats are sent every 5 seconds.

        Attributes:
            price (Union[Unset, ClientPrice]): The specification of an Account-specific Price.
            heartbeat (Union[Unset, PricingHeartbeat]): A PricingHeartbeat object is injected into the Pricing stream to
                ensure that the HTTP connection remains active.
    """

    price: Union[Unset, "ClientPrice"] = UNSET
    heartbeat: Union[Unset, "PricingHeartbeat"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        price: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.price, Unset):
            price = self.price.to_dict()

        heartbeat: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.heartbeat, Unset):
            heartbeat = self.heartbeat.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if price is not UNSET:
            field_dict["price"] = price
        if heartbeat is not UNSET:
            field_dict["heartbeat"] = heartbeat

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.pricing_heartbeat import PricingHeartbeat
        from ..models.client_price import ClientPrice

        d = src_dict.copy()
        _price = d.pop("price", UNSET)
        price: Union[Unset, ClientPrice]
        if isinstance(_price, Unset):
            price = UNSET
        else:
            price = ClientPrice.from_dict(_price)

        _heartbeat = d.pop("heartbeat", UNSET)
        heartbeat: Union[Unset, PricingHeartbeat]
        if isinstance(_heartbeat, Unset):
            heartbeat = UNSET
        else:
            heartbeat = PricingHeartbeat.from_dict(_heartbeat)

        stream_pricing_response_200 = cls(
            price=price,
            heartbeat=heartbeat,
        )

        stream_pricing_response_200.additional_properties = d
        return stream_pricing_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
