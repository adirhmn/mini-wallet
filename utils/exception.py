from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import status

class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

    def as_response(self):
        return JSONResponse(
            content = {
                "status" : "fail",
                "data": self.detail
            },
            status_code=self.status_code
        )

class CustomResponseValidationError():
    def __init__(self, exc: RequestValidationError):
        self.exc = exc
    
    def as_response(self):
        error = self.exc.errors()[0]
        if error["type"] != "missing":
            resp = self.exc.errors()
            err_resp = {
                "error" :resp
            }
        else:
            loc = error["loc"]
            err_field = loc[-1]
            err_resp = {
                "error" : {
                    err_field:[
                        "Missing data for required field."
                    ]
                }
            }
        raise CustomHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err_resp)

    