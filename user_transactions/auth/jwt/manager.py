from jwt import encode, decode, ExpiredSignatureError
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from os import getenv


SECRET_KEY :str = getenv("JWT_SECRET_KEY")

class JWTBearerManager(HTTPBearer):
    async def __call__(self, request: Request):
        
        try:
            auth = await super().__call__(request=request)
            request.state.user = validate_token(auth.credentials)
            
        except ExpiredSignatureError as e:
            print(f"[JWTBearerManager] invalid credentials {e}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
        
        

def create_token(data: dict) -> str:
    return encode(payload=data, key=SECRET_KEY, algorithm="HS256")


def validate_token(tok: str) -> dict:
    return decode(tok, key=SECRET_KEY, algorithms=["HS256"])