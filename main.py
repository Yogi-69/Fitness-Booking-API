from fastapi import FastAPI, Request
from routes import router
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


app = FastAPI(title="Fitness Booking API")

app.include_router(router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error = []

    for err in errors:
        if err.get("type") == "value_error.email":
            error.append("Invalid email address")
        else:
            loc = err.get("loc", [])
            field = loc[-1] if loc else "field"
            error.append(f"Missing or invalid value for '{field}'")

    return JSONResponse(
        status_code=422,
        content={"detail": error}
    )
