import datetime
import json
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.webhook_subscription_status_enum import WebhookSubscriptionStatusEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="WebhookSubscription")


@_attrs_define
class WebhookSubscription:
    """
    Attributes:
        id (int):
        tenant (int): The tenant (client) that owns this webhook subscription.
        events (List[int]): The events that the tenant has subscribed to for receiving webhooks.
        url (str): The URL where webhook payloads should be sent.
        secret (str): The secret key used to sign the webhook payload for validation purposes.
        created_at (datetime.datetime): The timestamp when the webhook subscription was created.
        updated_at (datetime.datetime): The timestamp when the webhook subscription was last updated.
        status (Union[Unset, WebhookSubscriptionStatusEnum]): * `active` - Active
            * `disabled` - Disabled
            * `suspended` - Suspended
        reason_disabled (Union[Unset, str]): Optional reason explaining why the subscription was disabled.
    """

    id: int
    tenant: int
    events: List[int]
    url: str
    secret: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    status: Union[Unset, WebhookSubscriptionStatusEnum] = UNSET
    reason_disabled: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        tenant = self.tenant

        events = self.events

        url = self.url

        secret = self.secret

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        reason_disabled = self.reason_disabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "tenant": tenant,
                "events": events,
                "url": url,
                "secret": secret,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if reason_disabled is not UNSET:
            field_dict["reason_disabled"] = reason_disabled

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        id = (None, str(self.id).encode(), "text/plain")

        tenant = (None, str(self.tenant).encode(), "text/plain")

        _temp_events = self.events
        events = (None, json.dumps(_temp_events).encode(), "application/json")

        url = (None, str(self.url).encode(), "text/plain")

        secret = (None, str(self.secret).encode(), "text/plain")

        created_at = self.created_at.isoformat().encode()

        updated_at = self.updated_at.isoformat().encode()

        status: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.status, Unset):
            status = (None, str(self.status.value).encode(), "text/plain")

        reason_disabled = (
            self.reason_disabled
            if isinstance(self.reason_disabled, Unset)
            else (None, str(self.reason_disabled).encode(), "text/plain")
        )

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "id": id,
                "tenant": tenant,
                "events": events,
                "url": url,
                "secret": secret,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if reason_disabled is not UNSET:
            field_dict["reason_disabled"] = reason_disabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        tenant = d.pop("tenant")

        events = cast(List[int], d.pop("events"))

        url = d.pop("url")

        secret = d.pop("secret")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        _status = d.pop("status", UNSET)
        status: Union[Unset, WebhookSubscriptionStatusEnum]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = WebhookSubscriptionStatusEnum(_status)

        reason_disabled = d.pop("reason_disabled", UNSET)

        webhook_subscription = cls(
            id=id,
            tenant=tenant,
            events=events,
            url=url,
            secret=secret,
            created_at=created_at,
            updated_at=updated_at,
            status=status,
            reason_disabled=reason_disabled,
        )

        webhook_subscription.additional_properties = d
        return webhook_subscription

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
