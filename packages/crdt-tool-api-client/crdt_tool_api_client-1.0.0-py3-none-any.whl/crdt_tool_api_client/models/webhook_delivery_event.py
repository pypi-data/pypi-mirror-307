import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.webhook_delivery_event_status_enum import WebhookDeliveryEventStatusEnum

T = TypeVar("T", bound="WebhookDeliveryEvent")


@_attrs_define
class WebhookDeliveryEvent:
    """
    Attributes:
        id (int):
        subscription (int): The webhook subscription associated with this delivery.
        event (int): The webhook event type that triggered this delivery.
        payload (Any): Stores the webhook payload sent to the client.
        response_status_code (Union[None, int]): The HTTP status code received from the client's response.
        response_body (str): The response body received from the client.
        status (WebhookDeliveryEventStatusEnum): * `pending` - Pending
            * `success` - Success
            * `failed` - Failed
        created_at (datetime.datetime): Date and time when the record was created.
        updated_at (datetime.datetime): Date and time when the record was last updated.
    """

    id: int
    subscription: int
    event: int
    payload: Any
    response_status_code: Union[None, int]
    response_body: str
    status: WebhookDeliveryEventStatusEnum
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        subscription = self.subscription

        event = self.event

        payload = self.payload

        response_status_code: Union[None, int]
        response_status_code = self.response_status_code

        response_body = self.response_body

        status = self.status.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "subscription": subscription,
                "event": event,
                "payload": payload,
                "response_status_code": response_status_code,
                "response_body": response_body,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        subscription = d.pop("subscription")

        event = d.pop("event")

        payload = d.pop("payload")

        def _parse_response_status_code(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        response_status_code = _parse_response_status_code(d.pop("response_status_code"))

        response_body = d.pop("response_body")

        status = WebhookDeliveryEventStatusEnum(d.pop("status"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        webhook_delivery_event = cls(
            id=id,
            subscription=subscription,
            event=event,
            payload=payload,
            response_status_code=response_status_code,
            response_body=response_body,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
        )

        webhook_delivery_event.additional_properties = d
        return webhook_delivery_event

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
