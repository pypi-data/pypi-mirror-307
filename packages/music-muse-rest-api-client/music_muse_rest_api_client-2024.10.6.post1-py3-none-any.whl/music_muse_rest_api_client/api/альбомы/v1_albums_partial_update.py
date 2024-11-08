from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.albums import Albums
from ...models.patched_albums_request import PatchedAlbumsRequest
from ...types import Response


def _get_kwargs(
    id: int,
    *,
    body: Union[
        PatchedAlbumsRequest,
        PatchedAlbumsRequest,
        PatchedAlbumsRequest,
    ],
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/api/v1/albums/{id}/",
    }

    if isinstance(body, PatchedAlbumsRequest):
        _json_body = body.to_dict()

        _kwargs["json"] = _json_body
        headers["Content-Type"] = "application/json"
    if isinstance(body, PatchedAlbumsRequest):
        _data_body = body.to_dict()

        _kwargs["data"] = _data_body
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, PatchedAlbumsRequest):
        _files_body = body.to_multipart()

        _kwargs["files"] = _files_body
        headers["Content-Type"] = "multipart/form-data"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Albums]:
    if response.status_code == 200:
        response_200 = Albums.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Albums]:
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
        PatchedAlbumsRequest,
        PatchedAlbumsRequest,
        PatchedAlbumsRequest,
    ],
) -> Response[Albums]:
    """
    Args:
        id (int):
        body (PatchedAlbumsRequest):
        body (PatchedAlbumsRequest):
        body (PatchedAlbumsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Albums]
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
        PatchedAlbumsRequest,
        PatchedAlbumsRequest,
        PatchedAlbumsRequest,
    ],
) -> Optional[Albums]:
    """
    Args:
        id (int):
        body (PatchedAlbumsRequest):
        body (PatchedAlbumsRequest):
        body (PatchedAlbumsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Albums
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
        PatchedAlbumsRequest,
        PatchedAlbumsRequest,
        PatchedAlbumsRequest,
    ],
) -> Response[Albums]:
    """
    Args:
        id (int):
        body (PatchedAlbumsRequest):
        body (PatchedAlbumsRequest):
        body (PatchedAlbumsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Albums]
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
        PatchedAlbumsRequest,
        PatchedAlbumsRequest,
        PatchedAlbumsRequest,
    ],
) -> Optional[Albums]:
    """
    Args:
        id (int):
        body (PatchedAlbumsRequest):
        body (PatchedAlbumsRequest):
        body (PatchedAlbumsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Albums
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
