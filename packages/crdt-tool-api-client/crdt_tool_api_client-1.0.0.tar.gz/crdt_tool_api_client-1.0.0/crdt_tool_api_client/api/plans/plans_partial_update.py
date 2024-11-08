from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.patched_plan import PatchedPlan
from ...models.plan import Plan
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: Union[
        PatchedPlan,
        PatchedPlan,
        PatchedPlan,
    ],
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/plans/{id}/",
    }

    if isinstance(body, PatchedPlan):
        _json_body = body.to_dict()

        _kwargs["json"] = _json_body
        headers["Content-Type"] = "application/json"
    if isinstance(body, PatchedPlan):
        _data_body = body.to_dict()

        _kwargs["data"] = _data_body
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, PatchedPlan):
        _files_body = body.to_multipart()

        _kwargs["files"] = _files_body
        headers["Content-Type"] = "multipart/form-data"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Plan]:
    if response.status_code == 200:
        response_200 = Plan.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Plan]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        PatchedPlan,
        PatchedPlan,
        PatchedPlan,
    ],
) -> Response[Plan]:
    """API endpoint that allows plans to be CRUDed.

    Args:
        id (str): Unique identifier for the plan.
        body (PatchedPlan): Serializer for the Plan model.
        body (PatchedPlan): Serializer for the Plan model.
        body (PatchedPlan): Serializer for the Plan model.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Plan]
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
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        PatchedPlan,
        PatchedPlan,
        PatchedPlan,
    ],
) -> Optional[Plan]:
    """API endpoint that allows plans to be CRUDed.

    Args:
        id (str): Unique identifier for the plan.
        body (PatchedPlan): Serializer for the Plan model.
        body (PatchedPlan): Serializer for the Plan model.
        body (PatchedPlan): Serializer for the Plan model.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Plan
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        PatchedPlan,
        PatchedPlan,
        PatchedPlan,
    ],
) -> Response[Plan]:
    """API endpoint that allows plans to be CRUDed.

    Args:
        id (str): Unique identifier for the plan.
        body (PatchedPlan): Serializer for the Plan model.
        body (PatchedPlan): Serializer for the Plan model.
        body (PatchedPlan): Serializer for the Plan model.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Plan]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        PatchedPlan,
        PatchedPlan,
        PatchedPlan,
    ],
) -> Optional[Plan]:
    """API endpoint that allows plans to be CRUDed.

    Args:
        id (str): Unique identifier for the plan.
        body (PatchedPlan): Serializer for the Plan model.
        body (PatchedPlan): Serializer for the Plan model.
        body (PatchedPlan): Serializer for the Plan model.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Plan
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
