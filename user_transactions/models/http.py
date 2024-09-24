from pydantic import BaseModel, Field

    

class HttpErrorResponse(BaseModel):
    error_details: str = Field(title="Error details", description="Additional data to understand error", default="")  
    retryable: bool = Field(title="Retryable request", description="Indicates if request can be retried", default=False)
