# TODO - remove this special case when we fix the generated code for empty openapi structs
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.operational_webhook_endpoint_update_metadata import OperationalWebhookEndpointUpdateMetadata


T = TypeVar("T", bound="OperationalWebhookEndpointUpdate")


@attr.s(auto_attribs=True)
class OperationalWebhookEndpointUpdate:
    """
    Attributes:
        url (str):  Example: https://example.com/webhook/.
        description (Union[Unset, str]):  Default: ''. Example: An example endpoint name.
        disabled (Union[Unset, bool]):
        filter_types (Union[Unset, None, List[str]]):  Example: ['message.attempt.failing'].
        metadata (Union[Unset, OperationalWebhookEndpointUpdateMetadata]):
        rate_limit (Union[Unset, None, int]):
        uid (Union[Unset, None, str]): Optional unique identifier for the endpoint Example: unique-ep-identifier.
    """

    url: str
    description: Union[Unset, str] = ""
    disabled: Union[Unset, bool] = False
    filter_types: Union[Unset, None, List[str]] = UNSET
    metadata: Union[Unset, "OperationalWebhookEndpointUpdateMetadata"] = UNSET
    rate_limit: Union[Unset, None, int] = UNSET
    uid: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url = self.url
        description = self.description
        disabled = self.disabled
        filter_types: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.filter_types, Unset):
            if self.filter_types is None:
                filter_types = None
            else:
                filter_types = self.filter_types

        metadata = self.metadata
        rate_limit = self.rate_limit
        uid = self.uid

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if disabled is not UNSET:
            field_dict["disabled"] = disabled
        if filter_types is not UNSET:
            field_dict["filterTypes"] = filter_types
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if rate_limit is not UNSET:
            field_dict["rateLimit"] = rate_limit
        if uid is not UNSET:
            field_dict["uid"] = uid

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        url = d.pop("url")

        description = d.pop("description", UNSET)

        disabled = d.pop("disabled", UNSET)

        filter_types = cast(List[str], d.pop("filterTypes", UNSET))

        metadata = d.pop("metadata", UNSET)

        rate_limit = d.pop("rateLimit", UNSET)

        uid = d.pop("uid", UNSET)

        operational_webhook_endpoint_update = cls(
            url=url,
            description=description,
            disabled=disabled,
            filter_types=filter_types,
            metadata=metadata,
            rate_limit=rate_limit,
            uid=uid,
        )

        operational_webhook_endpoint_update.additional_properties = d
        return operational_webhook_endpoint_update

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
