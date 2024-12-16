from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose import jwt

from Auth.jwt_token import create_access_jwt, create_refresh_jwt
from Database.Models import DatabaseModels

auth_scheme = OAuth2PasswordBearer(tokenUrl="/token")

error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")


async def authorize(token=Depends(auth_scheme)):
    try:
        data = jwt.decode(token, "", "HS256")
        if "username" not in data and "mode" not in data:
            raise error
        if data["mode"] != "refresh_token":
            return error
        user = await DatabaseModels.checkIfUserExists(data["user_name"])
        data = {"user_name": user.email}

        refresh_token = create_refresh_jwt(data)
        await DatabaseModels.updateRefrshTokenUser(refresh_token, 1)

        access_token = create_access_jwt(data)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "type": "bearer",
        }
    except JWTError:
        raise error


async def verified_user(token=Depends(auth_scheme)):
    try:
        data = jwt.decode(token, "", "HS256")
        if "username" not in data and "mode" not in data:
            raise error
        if data["mode"] != "access_token":
            return error
        user = await DatabaseModels.checkIfUserExists(data["user_name"])
        if user["status_code"] == 404:
            return error

        return user
    except JWTError:
        raise error
