import pandas as pd
from typing import Iterator
from pymongo.errors import BulkWriteError

from user_transactions.models.v1.transaction import Transaction


    
    
async def insert_transactions(itrecords: Iterator, datasize: int):
    
    insert_limit = 30
    data_to_insert = []
    
    for i in range(datasize):
        try:
            doc = next(itrecords)
            data_to_insert.append(Transaction(**doc))
            
            if len(data_to_insert) >= insert_limit or i == datasize -1:
                
                await Transaction.insert_many(data_to_insert)
                data_to_insert = []
        except BulkWriteError as e:
            data_to_insert = []