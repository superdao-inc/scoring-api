from fastapi import Request
from fastapi.responses import JSONResponse


async def value_error_exception_handler(
    request: Request, exc: ValueError
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )
