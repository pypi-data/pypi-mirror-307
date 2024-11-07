# TODO - remove this special case when we fix the generated code for empty openapi structs
from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="OperationalWebhookEndpointSecretOut")


@attr.s(auto_attribs=True)
class OperationalWebhookEndpointSecretOut:
    """
    Attributes:
        key (str): The endpoint's verification secret. If `null` is passed, a secret is automatically generated. Format:
            `base64` encoded random bytes optionally prefixed with `whsec_`. Recommended size: 24. Example:
            whsec_C2FVsBQIhrscChlQIMV+b5sSYspob7oD.
    """

    key: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        key = self.key

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key")

        operational_webhook_endpoint_secret_out = cls(
            key=key,
        )

        operational_webhook_endpoint_secret_out.additional_properties = d
        return operational_webhook_endpoint_secret_out

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
