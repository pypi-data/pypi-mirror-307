import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.schedule_shift_schema import ScheduleShiftSchema
from ...types import UNSET, Response, Unset


def _get_kwargs(
    schedule_id: int,
    *,
    datetime_start: datetime.datetime,
    datetime_end: datetime.datetime,
    overflow: Union[Unset, bool] = True,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_datetime_start = datetime_start.isoformat()
    params["datetime_start"] = json_datetime_start

    json_datetime_end = datetime_end.isoformat()
    params["datetime_end"] = json_datetime_end

    params["overflow"] = overflow

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/schedules/{schedule_id}/shifts/".format(
            schedule_id=schedule_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[List["ScheduleShiftSchema"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ScheduleShiftSchema.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[List["ScheduleShiftSchema"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    schedule_id: int,
    *,
    client: AuthenticatedClient,
    datetime_start: datetime.datetime,
    datetime_end: datetime.datetime,
    overflow: Union[Unset, bool] = True,
) -> Response[List["ScheduleShiftSchema"]]:
    """List Schedule Shifts

    Args:
        schedule_id (int):
        datetime_start (datetime.datetime):
        datetime_end (datetime.datetime):
        overflow (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ScheduleShiftSchema']]
    """

    kwargs = _get_kwargs(
        schedule_id=schedule_id,
        datetime_start=datetime_start,
        datetime_end=datetime_end,
        overflow=overflow,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    schedule_id: int,
    *,
    client: AuthenticatedClient,
    datetime_start: datetime.datetime,
    datetime_end: datetime.datetime,
    overflow: Union[Unset, bool] = True,
) -> Optional[List["ScheduleShiftSchema"]]:
    """List Schedule Shifts

    Args:
        schedule_id (int):
        datetime_start (datetime.datetime):
        datetime_end (datetime.datetime):
        overflow (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ScheduleShiftSchema']
    """

    return sync_detailed(
        schedule_id=schedule_id,
        client=client,
        datetime_start=datetime_start,
        datetime_end=datetime_end,
        overflow=overflow,
    ).parsed


async def asyncio_detailed(
    schedule_id: int,
    *,
    client: AuthenticatedClient,
    datetime_start: datetime.datetime,
    datetime_end: datetime.datetime,
    overflow: Union[Unset, bool] = True,
) -> Response[List["ScheduleShiftSchema"]]:
    """List Schedule Shifts

    Args:
        schedule_id (int):
        datetime_start (datetime.datetime):
        datetime_end (datetime.datetime):
        overflow (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ScheduleShiftSchema']]
    """

    kwargs = _get_kwargs(
        schedule_id=schedule_id,
        datetime_start=datetime_start,
        datetime_end=datetime_end,
        overflow=overflow,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    schedule_id: int,
    *,
    client: AuthenticatedClient,
    datetime_start: datetime.datetime,
    datetime_end: datetime.datetime,
    overflow: Union[Unset, bool] = True,
) -> Optional[List["ScheduleShiftSchema"]]:
    """List Schedule Shifts

    Args:
        schedule_id (int):
        datetime_start (datetime.datetime):
        datetime_end (datetime.datetime):
        overflow (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ScheduleShiftSchema']
    """

    return (
        await asyncio_detailed(
            schedule_id=schedule_id,
            client=client,
            datetime_start=datetime_start,
            datetime_end=datetime_end,
            overflow=overflow,
        )
    ).parsed
