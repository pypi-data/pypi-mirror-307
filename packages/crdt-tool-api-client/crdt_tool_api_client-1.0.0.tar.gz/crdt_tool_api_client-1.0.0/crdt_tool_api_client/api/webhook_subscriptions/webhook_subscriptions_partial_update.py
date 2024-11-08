from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.patched_webhook_subscription import PatchedWebhookSubscription
from ...models.webhook_subscription import WebhookSubscription
from ...types import Response


def _get_kwargs(
    id: int,
    *,
    body: Union[
        PatchedWebhookSubscription,
        PatchedWebhookSubscription,
        PatchedWebhookSubscription,
    ],
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/webhook-subscriptions/{id}/",
    }

    if isinstance(body, PatchedWebhookSubscription):
        _json_body = body.to_dict()

        _kwargs["json"] = _json_body
        headers["Content-Type"] = "application/json"
    if isinstance(body, PatchedWebhookSubscription):
        _data_body = body.to_dict()

        _kwargs["data"] = _data_body
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, PatchedWebhookSubscription):
        _files_body = body.to_multipart()

        _kwargs["files"] = _files_body
        headers["Content-Type"] = "multipart/form-data"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[WebhookSubscription]:
    if response.status_code == 200:
        response_200 = WebhookSubscription.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[WebhookSubscription]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: int,
    *,
    client: AuthenticatedClient,
    body: Union[
        PatchedWebhookSubscription,
        PatchedWebhookSubscription,
        PatchedWebhookSubscription,
    ],
) -> Response[WebhookSubscription]:
    """API endpoint that allows CRUD operations on Webhook Subscriptions.

    Args:
        id (int):
        body (PatchedWebhookSubscription):
        body (PatchedWebhookSubscription):
        body (PatchedWebhookSubscription):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WebhookSubscription]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    *,
    client: AuthenticatedClient,
    body: Union[
        PatchedWebhookSubscription,
        PatchedWebhookSubscription,
        PatchedWebhookSubscription,
    ],
) -> Optional[WebhookSubscription]:
    """API endpoint that allows CRUD operations on Webhook Subscriptions.

    Args:
        id (int):
        body (PatchedWebhookSubscription):
        body (PatchedWebhookSubscription):
        body (PatchedWebhookSubscription):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WebhookSubscription
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient,
    body: Union[
        PatchedWebhookSubscription,
        PatchedWebhookSubscription,
        PatchedWebhookSubscription,
    ],
) -> Response[WebhookSubscription]:
    """API endpoint that allows CRUD operations on Webhook Subscriptions.

    Args:
        id (int):
        body (PatchedWebhookSubscription):
        body (PatchedWebhookSubscription):
        body (PatchedWebhookSubscription):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WebhookSubscription]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    *,
    client: AuthenticatedClient,
    body: Union[
        PatchedWebhookSubscription,
        PatchedWebhookSubscription,
        PatchedWebhookSubscription,
    ],
) -> Optional[WebhookSubscription]:
    """API endpoint that allows CRUD operations on Webhook Subscriptions.

    Args:
        id (int):
        body (PatchedWebhookSubscription):
        body (PatchedWebhookSubscription):
        body (PatchedWebhookSubscription):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WebhookSubscription
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
