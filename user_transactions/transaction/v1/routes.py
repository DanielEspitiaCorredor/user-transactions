from fastapi import Request, APIRouter, Depends, status
from fastapi.responses import JSONResponse


from user_transactions.models.v1.transaction import ExtractRequest
from user_transactions.transaction.v1 import process
from user_transactions.auth.jwt.manager import JWTBearerManager

import pandas as pd


# Transactions router
tx_router = APIRouter(
    prefix="/v1/transactions",
    dependencies=[Depends(JWTBearerManager())]
)


@tx_router.post("/generate_report")
def generate_report(extract_data: ExtractRequest, request: Request):
    
    
    process_msg = f"[{request.state.request_id}][Generate_report]"
    
    print(f"{process_msg} Extract data process")
    
    process.generate_report(extract_data)
    
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)