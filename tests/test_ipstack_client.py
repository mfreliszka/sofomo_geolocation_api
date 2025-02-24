"""Module containing tests for IpstackClient error handling."""

import pytest
import httpx
from fastapi import HTTPException, status
from app.clients import IpstackClient
from unittest.mock import AsyncMock


@pytest.mark.parametrize(
    "error_code, expected_status, expected_message",
    [
        (404, 404, "The requested resource does not exist."),
        (101, 401, "Invalid or missing API key."),
        (102, 403, "User account is inactive. Contact Customer Support."),
        (103, 400, "Invalid API function."),
        (104, 402, "Usage limit reached."),
        (106, 400, "The IP Address supplied is invalid."),
        (301, 400, "Invalid fields parameter."),
        (302, 400, "Too many IPs specified for Bulk Lookup."),
        (303, 403, "Batch lookup not supported on this plan."),
        (999, 500, "Unknown error occurred."),  # Unmapped error
    ],
)
@pytest.mark.anyio
async def test_get_geolocation_ipstack_errors(
    mocker, error_code, expected_status, expected_message
):
    """Test mapped error responses from IpstackClient.get_geolocation."""

    mock_response = AsyncMock(spec=httpx.Response)
    mock_response.json.return_value = {
        "success": False,
        "error": {"code": error_code, "info": expected_message},
    }
    mock_response.status_code = expected_status
    mock_response.raise_for_status = AsyncMock()

    mocker.patch.object(httpx.AsyncClient, "get", return_value=mock_response)

    async with IpstackClient() as client:
        with pytest.raises(HTTPException) as exc_info:
            await client.get_geolocation("8.8.8.8")

    assert exc_info.value.status_code == expected_status
    assert expected_message in exc_info.value.detail


@pytest.mark.anyio
async def test_get_geolocation_timeout(mocker):
    """Test handling of a timeout exception."""
    mocker.patch.object(
        httpx.AsyncClient,
        "get",
        side_effect=httpx.TimeoutException("Request timed out"),
    )

    async with IpstackClient() as client:
        with pytest.raises(HTTPException) as exc_info:
            await client.get_geolocation("8.8.8.8")

    assert exc_info.value.status_code == status.HTTP_504_GATEWAY_TIMEOUT
    assert "Request timed out" in exc_info.value.detail
