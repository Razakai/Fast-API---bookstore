from passlib.context import CryptContext
from models.jwtUser import JWTUser
from datetime import datetime, timedelta
from utils.const import JWT_EXPIRATION_TIME_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import time

passwordContext = CryptContext(schemes=["bcrypt"])
oauthSchema = OAuth2PasswordBearer(tokenUrl="/token")

jwtUser1 = {"username": "adam", "password": "$2b$12$k48MpVizzZzn5LdDyzhaTeGsoHkui5e7hfD8LdpXM2A0uaSZfnmrW", "disabled": False, "role": "admin"}
jwtUserFakeDB = JWTUser(**jwtUser1)


def getHashedPassword(password):
    return passwordContext.hash(password)


def verifyPassword(password, hashPassword):
    try:
        return passwordContext.verify(password, hashPassword)
    except Exception as e:
        return False


# Authenticate username and password to give JWT token
def authenticateUser(user: JWTUser):
    if jwtUserFakeDB.username == user.username:
        if verifyPassword(user.password, jwtUserFakeDB.password):
            user.role = "admin"
            return user
    return None


# Create access JWT token
def createJWTToken(user: JWTUser):
    exp = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    payload = {
        "sub": user.username,
        "role": user.role,
        "exp": exp,
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


# Check weather JWT token is correct
def checkJWTToken(token: str = Depends(oauthSchema)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
        username = payload.get("sub")
        role = payload.get("role")
        exp = payload.get("exp")
        if time.time() < exp:
            if jwtUserFakeDB.username == username:
                return finalChecks(role)
    except Exception as e:
        return False

    return False


# Last checking and returning final result
def finalChecks(role: str):
    return role == "admin"