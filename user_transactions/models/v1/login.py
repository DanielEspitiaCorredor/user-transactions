from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(title="Username", description="A valid username value",  min_length=5, example="despitia")
    password: str = Field(title="Password", description="Security password",  min_length=5, example="despitia#123")
    
    


class LoginResponse(BaseModel):
    token: str = Field(title="Token", description="A valid JWT")
    exp: str = Field(title="Token expiration", description="Token expiration date")