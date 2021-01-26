from fastapi import FastAPI, Body, Header, File, Depends, HTTPException
from models.User import User
from models.Author import Author
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from starlette.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from utils.security import authenticateUser, createJWTToken
from models.jwtUser import JWTUser


server_v1 = FastAPI(openapi_prefix="/v1")


@server_v1.get("/")
async def helloWorld():
    return {"Hello world!"}


@server_v1.post("/user", status_code=HTTP_201_CREATED)
async def createUser(user: User):
    return {"request body": user}


@server_v1.get("/user")
async def getUserValidation(password: str):
    return {"parameter": password}


@server_v1.get("/book/{isbn}")
async def getBook(isbn: str):
    return {"query parameter": isbn}


@server_v1.get("/author/{id}/book")
async def getAuthorBook(id: int, category: str, order: str = "asc"):
    return {"query parameters": str(id) + category + order}


@server_v1.patch("/author/name")
async def updateAuthorName(name: str = Body(..., embed=True)):
    return {"query name": name}


@server_v1.post("/user/author")
async def postUserAndAuthor(user: User, author: Author, bookstore: str = Body(..., embed=True)):
    return {
        "user": user,
        "author": author,
        "store": bookstore
    }


# headers example
@server_v1.post("/user/headersexample")
async def createUser(user: User, customHeaders: str = Header("default")):
    return {
        "request body": user,
        "headers": customHeaders
    }


# files

@server_v1.post("/user/photo")
async def uploadUserPhoto(response: Response, profilePhoto: bytes = File(...)):
    response.headers["file-size"] = str(len(profilePhoto))
    return {"File size": len(profilePhoto)}


# Testing JWT in endpoint
@server_v1.post("/token")
async def loginForAccessToken(form_data: OAuth2PasswordRequestForm = Depends()):
    jwtUserDict = {"username": form_data.username, "password": form_data.password}
    print(jwtUserDict)
    jwtUser = JWTUser(**jwtUserDict)

    user = authenticateUser(jwtUser)
    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    jwt_token = createJWTToken(user)
    return {"token": jwt_token}