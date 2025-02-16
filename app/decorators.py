"""Module containing decorators for the geolocation API."""

from functools import wraps
from fastapi import HTTPException

# Error mapping based on IPStack documentation
ERROR_CODES_MAPPING = {
    404: (404, "The requested resource does not exist."),
    101: (401, "Invalid or missing API key."),
    102: (403, "User account is inactive. Contact Customer Support."),
    103: (400, "Invalid API function."),
    104: (402, "Usage limit reached."),
    301: (400, "Invalid fields parameter."),
    302: (400, "Too many IPs specified for Bulk Lookup."),
    303: (403, "Batch lookup not supported on this plan."),
}


def handle_ipstack_errors(func):
    """Decorator to handle errors from IPStack API."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        data = await func(*args, **kwargs)

        if isinstance(data, dict) and "success" in data and not data["success"]:
            error_info = data.get("error", {})
            error_code = error_info.get("code", 500)
            error_message = error_info.get("info", "Unknown error occurred.")

            status_code, mapped_message = ERROR_CODES_MAPPING.get(
                error_code, (500, error_message)
            )
            raise HTTPException(status_code=status_code, detail=mapped_message)

        return data

    return wrapper
