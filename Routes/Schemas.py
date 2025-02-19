from typing import Any
from pydantic import BaseModel, Field, EmailStr


class NewUserSchema(BaseModel):
    USER_ID: str = Field()
    F_NAME: str = Field()
    L_NAME:str = Field()
    PASSX: str = Field()
    EMAIL: EmailStr = Field()
    AUTHYPE: str = Field(default=None)


class Phase1loginSchema(BaseModel):
    login_email: str = Field()
    login_password: str = Field()


class otpSchema(BaseModel):
    user_email: EmailStr = Field()
    attempt: int = Field()


class checkUsernameSchema(BaseModel):
    user_name: str = Field()


class checkEmailRegistrySchema(BaseModel):
    email: str = Field()


class genImageSchema(BaseModel):
    prompt: str = Field()


class Phase2loginSchema(BaseModel):
    otp: int = Field()
    user_email: EmailStr = Field()
