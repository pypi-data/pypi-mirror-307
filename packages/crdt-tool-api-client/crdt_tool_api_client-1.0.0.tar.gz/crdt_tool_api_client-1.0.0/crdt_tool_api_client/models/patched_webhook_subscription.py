import datetime
import json
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.webhook_subscription_status_enum import WebhookSubscriptionStatusEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedWebhookSubscription")


@_attrs_define
class PatchedWebhookSubscription:
    """
    Attributes:
        id (Union[Unset, int]):
        tenant (Union[Unset, int]): The tenant (client) that owns this webhook subscription.
        events (Union[Unset, List[int]]): The events that the tenant has subscribed to for receiving webhooks.
        url (Union[Unset, str]): The URL where webhook payloads should be sent.
        secret (Union[Unset, str]): The secret key used to sign the webhook payload for validation purposes.
        status (Union[Unset, WebhookSubscriptionStatusEnum]): * `active` - Active
            * `disabled` - Disabled
            * `suspended` - Suspended
        reason_disabled (Union[Unset, str]): Optional reason explaining why the subscription was disabled.
        created_at (Union[Unset, datetime.datetime]): The timestamp when the webhook subscription was created.
        updated_at (Union[Unset, datetime.datetime]): The timestamp when the webhook subscription was last updated.
    """

    id: Union[Unset, int] = UNSET
    tenant: Union[Unset, int] = UNSET
    events: Union[Unset, List[int]] = UNSET
    url: Union[Unset, str] = UNSET
    secret: Union[Unset, str] = UNSET
    status: Union[Unset, WebhookSubscriptionStatusEnum] = UNSET
    reason_disabled: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        tenant = self.tenant

        events: Union[Unset, List[int]] = UNSET
        if not isinstance(self.events, Unset):
            events = self.events

        url = self.url

        secret = self.secret

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        reason_disabled = self.reason_disabled

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if tenant is not UNSET:
            field_dict["tenant"] = tenant
        if events is not UNSET:
            field_dict["events"] = events
        if url is not UNSET:
            field_dict["url"] = url
        if secret is not UNSET:
            field_dict["secret"] = secret
        if status is not UNSET:
            field_dict["status"] = status
        if reason_disabled is not UNSET:
            field_dict["reason_disabled"] = reason_disabled
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        id = self.id if isinstance(self.id, Unset) else (None, str(self.id).encode(), "text/plain")

        tenant = self.tenant if isinstance(self.tenant, Unset) else (None, str(self.tenant).encode(), "text/plain")

        events: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.events, Unset):
            _temp_events = self.events
            events = (None, json.dumps(_temp_events).encode(), "application/json")

        url = self.url if isinstance(self.url, Unset) else (None, str(self.url).encode(), "text/plain")

        secret = self.secret if isinstance(self.secret, Unset) else (None, str(self.secret).encode(), "text/plain")

        status: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.status, Unset):
            status = (None, str(self.status.value).encode(), "text/plain")

        reason_disabled = (
            self.reason_disabled
            if isinstance(self.reason_disabled, Unset)
            else (None, str(self.reason_disabled).encode(), "text/plain")
        )

        created_at: Union[Unset, bytes] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat().encode()

        updated_at: Union[Unset, bytes] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat().encode()

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if tenant is not UNSET:
            field_dict["tenant"] = tenant
        if events is not UNSET:
            field_dict["events"] = events
        if url is not UNSET:
            field_dict["url"] = url
        if secret is not UNSET:
            field_dict["secret"] = secret
        if status is not UNSET:
            field_dict["status"] = status
        if reason_disabled is not UNSET:
            field_dict["reason_disabled"] = reason_disabled
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        tenant = d.pop("tenant", UNSET)

        events = cast(List[int], d.pop("events", UNSET))

        url = d.pop("url", UNSET)

        secret = d.pop("secret", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, WebhookSubscriptionStatusEnum]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = WebhookSubscriptionStatusEnum(_status)

        reason_disabled = d.pop("reason_disabled", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        patched_webhook_subscription = cls(
            id=id,
            tenant=tenant,
            events=events,
            url=url,
            secret=secret,
            status=status,
            reason_disabled=reason_disabled,
            created_at=created_at,
            updated_at=updated_at,
        )

        patched_webhook_subscription.additional_properties = d
        return patched_webhook_subscription

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
