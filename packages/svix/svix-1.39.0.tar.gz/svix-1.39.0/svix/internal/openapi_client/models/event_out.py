# TODO - remove this special case when we fix the generated code for empty openapi structs
import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="EventOut")


@attr.s(auto_attribs=True)
class EventOut:
    """
    Attributes:
        payload (str):
        timestamp (datetime.datetime):
    """

    payload: str
    timestamp: datetime.datetime
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = self.payload
        timestamp = self.timestamp.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "payload": payload,
                "timestamp": timestamp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        payload = d.pop("payload")

        timestamp = isoparse(d.pop("timestamp"))

        event_out = cls(
            payload=payload,
            timestamp=timestamp,
        )

        event_out.additional_properties = d
        return event_out

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
