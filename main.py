from fastapi import FastAPI
from os import getenv


from motor.motor_asyncio import AsyncIOMotorClient
from user_transactions.models.definitions import document_models_v1
from user_transactions.auth.v1.authentication import auth_router
from user_transactions.middlewares.request import RequestDataMiddleware
from beanie import init_beanie

async def app_lifespan(app: FastAPI):
    # Configure mongo database
    print("Start with app configurations")
    db_name : str = getenv("DB_NAME") 
    connection_uri :str = getenv("DB_MONGO_URI")
    
    if not db_name:
        raise Exception("Missing environment var DB_NAME")
    if not connection_uri:
        raise Exception("Missing environment var DB_MONGO_URI")
    
    
    
    app.mongodb_client = AsyncIOMotorClient(connection_uri)
    app.database = app.mongodb_client[db_name]
    
    ping_response = await app.database.command("ping")
    
    if int(ping_response["ok"]) != 1: 
        raise Exception("Problem connecting to database")

    print(f"Connected to mongoDB {db_name}")
    
    
     # INIT BEANIE
    await init_beanie(
        app.database,
        document_models=document_models_v1,
    )
    yield
    
    app.mongodb_client.close()

app = FastAPI(lifespan=app_lifespan)
app.title = "Api used to manage user transactions"
app.add_middleware(RequestDataMiddleware)

# Routers
app.include_router(auth_router)