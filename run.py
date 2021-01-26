from fastapi import FastAPI
from routes.v1 import server_v1
from routes.v2 import server_v2
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED
from utils.security import checkJWTToken

server = FastAPI()

server.mount("/v1", server_v1)
server.mount("/v2", server_v2)

@server.middleware("http")
async def middleware(request: Request, callNext):
    if not any(word in str(request.url) for word in ["/token", "/docs", "/openapi.json"]):
        try:
            jwtToken = request.headers["Authorization"].split(" ")[1]
            print(jwtToken)
            if not checkJWTToken(jwtToken):
                return Response("Unauthorized", status_code=HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response("Unauthorized", status_code=HTTP_401_UNAUTHORIZED)

    response = await callNext(request)
    return response
