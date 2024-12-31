from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utilities.hash import Hash


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.hash_util = Hash()

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid Scheme")
            if not self.verify_jwt(credentials.credentials):
                print(credentials.credentials)
                raise HTTPException(
                    status_code=403, detail="Invalid Authorization Token"
                )
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid Authorization Code")

    def verify_jwt(self, jwt_token: str) -> bool:
        try:
            payload = self.hash_util.decodeJWT(jwt_token)
            if payload and "sub" in payload:
                return True
            return False
        except Exception as e:
            print(f"Token verification failed with error: {e}")
            return False
