from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from routers import router as predict_router


app = FastAPI(title="Advertisement moderation")
app.include_router(predict_router)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Invalid request",
            "errors": [
                {"loc": error["loc"], "msg": error["msg"]}
                for error in exc.errors()
            ],
        },
    )


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}
