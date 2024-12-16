from typing import Any
from pydantic import BaseModel, Field, EmailStr


class NewUserSchema(BaseModel):
    USER_ID: str = Field()
    F_NAME: str = Field()
    PASSX: str = Field()
    EMAIL: EmailStr = Field()


class Phase1loginSchema(BaseModel):
    login_email: str = Field()
    login_password: str = Field()

class otpSchema(BaseModel):
    user_email: EmailStr = Field()

class Phase2loginSchema(BaseModel):
    user_email: EmailStr = Field()
    otp: int = Field()
