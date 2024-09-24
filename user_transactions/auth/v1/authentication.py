from typing import Annotated, Union

from fastapi import Request, APIRouter,  Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from user_transactions.models.v1.user import UserRequest, User, UserResponse
from user_transactions.models.v1.login import LoginRequest
from user_transactions.auth.v1.errors import RegisterConflict
from user_transactions.auth.v1.security import get_hashed_password
from user_transactions.models.http import  HttpErrorResponse
from uuid import uuid4

# verify_access_token


auth_router = APIRouter(
    prefix="/v1/auth"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@auth_router.post("/register")
async def register(user: UserRequest, request: Request):
    
    try: 
        process_msg = f"[{request.state.request_id}][Register]"
        
        print(f"{process_msg} Start process")
        
        count = await User.find_one(User.username == user.username).count()
        
        if count > 0:
            raise RegisterConflict("user already exist")
            
        
        user_data = user.model_copy().model_dump()
        user_data["hashed_password"] = get_hashed_password(user.password)
        record = User(**user_data)
        
        userdb = await User.insert_one(record)
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=UserResponse(**userdb.model_dump()).model_dump())
    
    
    except RegisterConflict:
        print(f"{process_msg}[ERROR] User already exist")
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=HttpErrorResponse(
                error_details="cannot create this user",
                retryable=False
            ).model_dump())
        
    except Exception as e:
        
        print(f"{process_msg}[ERROR] Unexpected exception {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=HttpErrorResponse(
                error_details="unexpected exception",
                retryable=True
            ).model_dump())



