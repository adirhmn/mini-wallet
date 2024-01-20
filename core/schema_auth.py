from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, Request, status

class OAuth2Token(OAuth2PasswordBearer):
    def __init__(
        self,
        tokenUrl: str = "token",
        scheme_name: str = None,
        auto_error: bool = True,
    ):
        super().__init__(tokenUrl=tokenUrl, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None

        scheme, param = authorization.split()
        if scheme.lower() == "token":
            return param

        if self.auto_error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            return None
