from fastapi import FastAPI
from api.api import api_router
from db.session import engine, Base
from utils.exception import CustomHTTPException, CustomResponseValidationError
from fastapi import Request
from fastapi.exceptions import RequestValidationError

# Create tables in database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

# Import api route from api_router
app.include_router(api_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return CustomResponseValidationError(exc).as_response()


@app.exception_handler(CustomHTTPException)
async def custom_http_exception_handler(request, exc: CustomHTTPException):
    return exc.as_response()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)