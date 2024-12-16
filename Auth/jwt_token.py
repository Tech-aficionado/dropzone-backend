from jose import jwt
from datetime import datetime, timedelta

SECRET = (
    "e2ba563d5638da4cb3fe296290357ed69aebbf49c86e1f31b23aada3b491141eee538c9fd5439ec88"
)


def create_access_jwt(data: dict):
    data["exp"] = datetime.utcnow() + timedelta(days=1)
    data["mode"] = "access_token"
    return jwt.encode(data, SECRET, "HS256")


def create_refresh_jwt(data: dict):
    data["exp"] = datetime.utcnow() + timedelta(days=360)
    data["mode"] = "refresh_token"
    return jwt.encode(data, SECRET, "HS256")
