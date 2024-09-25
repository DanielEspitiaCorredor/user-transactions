from fastapi import Request, APIRouter, status
from fastapi.responses import JSONResponse
from user_transactions.models.v1.user import UserRequest, User, UserResponse
from user_transactions.models.v1.login import LoginRequest, LoginResponse
from user_transactions.auth.v1.errors import RegisterConflict
from user_transactions.auth.v1.security import get_hashed_password, is_correct_password
from user_transactions.models.http import  HttpErrorResponse
from user_transactions.auth.jwt.manager import create_token
from uuid import uuid4
from datetime import datetime, timezone, timedelta

# verify_access_token


auth_router = APIRouter(
    prefix="/v1/auth"
)

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



@auth_router.post("/login")
async def login(login: LoginRequest, request: Request):
    
    process_msg = f"[{request.state.request_id}][Login]"
    
    print(f"{process_msg} Start process")
    
    user = await User.find_one(User.username == login.username)
        
    if not user:
        print(f"{process_msg}[ERROR] User not found")
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=HttpErrorResponse(
                error_details="invalid username or password",
                retryable=False
            ).model_dump())
    
    
    if is_correct_password(login.password, user.hashed_password):
        tkn_data = user.model_dump(exclude=['hashed_password'])
        tkn_data["exp"] = datetime.now(tz=timezone.utc) + timedelta(hours=1)
        tkn = create_token(tkn_data)
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=LoginResponse(token=tkn,
                                                                                  exp=tkn_data["exp"].isoformat(timespec='milliseconds')).model_dump())
        
    
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=HttpErrorResponse(
            error_details="invalid username or password",
            retryable=False
        ).model_dump())