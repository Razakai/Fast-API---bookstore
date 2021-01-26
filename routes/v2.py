from fastapi import FastAPI
from models.User import User
from starlette.status import HTTP_201_CREATED

server_v2 = FastAPI(openapi_prefix="/v2")

@server_v2.get("/")
async def helloWorld():
    return {"Hello world!"}


@server_v2.post("/user", status_code=HTTP_201_CREATED)
async def createUser(user: User):
    return {"request body": user}