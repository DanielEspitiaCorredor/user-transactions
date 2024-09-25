
from pydantic import BaseModel, Field, field_serializer
from beanie import  Document

from datetime import datetime, timezone


class ExtractRequest(BaseModel):
    account: str = Field(title="Account", description="User account", example="976133242399")
    year: int = Field(title="Year", description="A valid year to extract data", example=2024)
    receiver_email: str = Field(title="Receiver Email", description="Email to receive account report", example="danielespitiacorredor@gmail.com")



class Transaction(Document):
    id : int
    date: datetime = Field(title="Transaction date", description="Explain itself")
    name: str = Field(title="Transaction Name", description="Explain itself")
    value: float = Field(title="Transaction Name", description="Explain itself")
    created_at: datetime = Field(title="created date", description="Explain itself", default=datetime.now(timezone.utc))
    
    
    @field_serializer('date')
    def serialize_transaction_date(self, dt: datetime, _info):
        return dt.strftime('%Y-%m-%d')
    
    @field_serializer('created_at')
    def serialize_created_at(self, dt: datetime, _info):
        return dt.isoformat(timespec='milliseconds')
        
    class Settings:
        # The name of the collection to store these objects.
        name = "transactions"
        
        
