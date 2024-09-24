from pydantic import (BaseModel, Field, EmailStr, field_serializer)
from datetime import datetime, timezone
from beanie import  Document


class UserRequest(BaseModel):
    username: str = Field(title="Username", description="A valid username value",  min_length=5, max_length=15, example="despitia")
    email: EmailStr = Field(title="Email Address", description="A valid email address", example="despitia@example.com")
    name: str = Field(title="Name", description="User full name", example="Daniel Espitia")
    password: str = Field(title="Password", description="Security password",  min_length=5, max_length=30, example="despitia#123")
    


class User(Document):
    username : str
    email: EmailStr
    name: str
    hashed_password: str
    disabled: bool = False
    created_at: datetime = Field(title="Update date", description="Explain itself", default=datetime.now(timezone.utc))
    updated_at: datetime = Field(title="Creation date", description="Explain itself", default=datetime.now(timezone.utc))
    
    @field_serializer('created_at', 'updated_at')
    def serialize_date(self, dt: datetime, _info):
        return dt.isoformat(timespec='milliseconds')
        
    class Settings:
        # The name of the collection to store these objects.
        name = "users"


class UserResponse(BaseModel):
    username: str
    email: EmailStr
    name: str
    disabled: bool
    created_at: datetime
    
    @field_serializer('created_at')
    def serialize_created_at(self, dt: datetime, _info):
        return dt.isoformat(timespec='milliseconds')