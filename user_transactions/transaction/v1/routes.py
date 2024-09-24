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


@tx_router.post("/extract")
async def extract(extract_data: ExtractRequest, request: Request):
    
    
    process_msg = f"[{request.state.request_id}][Extract]"
    
    print(f"{process_msg} Extract data process")
    
    await process.extract_and_insert_data(extract_data)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={})