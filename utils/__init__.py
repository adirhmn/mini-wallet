from fastapi import HTTPException
from fastapi.responses import JSONResponse

class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

    def as_response(self):
        return JSONResponse(
            content = {
                "status" : "failed",
                "message": self.detail
            },
            status_code=self.status_code
        )