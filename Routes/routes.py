import base64
import io
import json
import time
from typing import Any, Dict
from Auth.authorize import authorize, verified_user
from Auth.authapikey import pwd_context
from Auth.jwt_token import create_access_jwt, create_refresh_jwt
from Database.Models import DatabaseModels
from Routes.Schemas import (
    NewUserSchema,
    Phase1loginSchema,
    Phase2loginSchema,
    checkEmailRegistrySchema,
    checkUsernameSchema,
    genImageSchema,
    otpSchema,
)
from fastapi import APIRouter, Depends, Request, status, HTTPException

from services.emailService import OtpVerificationMailingService
from services.otpGenerator import ManageOtp

# -----------------------Users--------------------------------
Usersroute = APIRouter(prefix="/jholi-services/users", tags=["USERS"])


@Usersroute.post("/newUser")
async def root(userdetails: NewUserSchema):
    try:
        userdetails.PASSX = pwd_context.hash(userdetails.PASSX)

        data = userdetails.model_dump()
        data.__setitem__('AUTHYPE','native')

        email_exist = DatabaseModels.checkIfUserExists(data["EMAIL"])
        if email_exist != 404:
            return HTTPException(
                status_code=status.HTTP_208_ALREADY_REPORTED,
                detail="User Already Exists",
            )
        
        
        user_obj = DatabaseModels.createNewUser(data)
        if user_obj["row"] > 0:
            OtpVerificationMailingService(data['EMAIL']).onBoarding(data['F_NAME'])
            return HTTPException(
                status_code=status.HTTP_201_CREATED, detail="User Created... Proceed to verfiy"
            )
        
        else:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something Went Wrong",
            )
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=(e)
        )


@Usersroute.post("/phase1loginAuth", status_code=status.HTTP_200_OK)
async def existingUser(user: Phase1loginSchema):
    try:
        if (
            user.login_email == " "
            or user.login_password == " "
            or user.login_email is None
            or user.login_password is None
            or user.login_email == ""
            or user.login_password == ""
        ):
            return HTTPException(
                status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                detail="No Valid User Details",
            )
        fetchedUser = DatabaseModels.checkIfUserExists(user.login_email)
        if fetchedUser == 404:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found!!!"
            )

        check1 = pwd_context.verify(
            user.login_password, fetchedUser.get("details")[0].get("PASS_X")
        )
        if not check1:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password Didn't Match!!",
            )

        check2: bool = fetchedUser.get("details")[0].get("AUTHYPE") == "native"
        if not check2:
            return HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Registered with different method!!",
            )
        time.sleep(4)
        return {
            "message": "Phase 1 Successful",
            "status_code": status.HTTP_202_ACCEPTED,
        }
    finally:
        pass


@Usersroute.post("/refreshToken")
async def refresh(token_data: dict = Depends(authorize)):
    return token_data


@Usersroute.post("/activateOtp")
async def sendotp(user_email: otpSchema):
    email = user_email.user_email
    OtpVerificationMailingService(email).sendOtp()

    return {"message": "Otp Sent", "statuscode": 200}


@Usersroute.post("/checkUsername")
async def checkUsername(user_name: checkUsernameSchema):
    user = user_name.user_name
    username = DatabaseModels.checkIfUsernameExists(user)
    return username


@Usersroute.post("/checkEmailRegistry")
async def checkEmailRegistry(email: checkEmailRegistrySchema):
    email = email.email
    email = DatabaseModels.checkIfEmailRegistered(email)
    return email


@Usersroute.post("/phase2loginAuth")
async def sendotp(user: Phase2loginSchema):
    valid = ManageOtp.otpVerification(user.otp, user.user_email)
    if valid is False:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Otp Not Verified",
        )

    data = {"email": user.user_email}
    response = DatabaseModels.updateVerification(1,user.user_email)
    access_token = create_access_jwt(data)
    print(access_token)

    refresh_token = create_refresh_jwt(data)
    # store_refresh_token = DatabaseModels.updateRefrshTokenUser(
    #     refresh_token, 1, user.user_email
    # )
    # if store_refresh_token.get("row") == 0:
    #     return HTTPException(
    #     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #     detail="Refresh Token Error!!",
    #     )

    return {
        "message": "Login Successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "type": "bearer",
        "status_code": status.HTTP_200_OK,
    }


@Usersroute.post("/auth/prompted/profilePic", status_code=status.HTTP_200_OK)
async def getProfilePic(prompt: genImageSchema):
    from huggingface_hub import InferenceClient

    client = InferenceClient(
        "stabilityai/stable-diffusion-3.5-large",
        token="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",
    )

    image = client.text_to_image(prompt=prompt.prompt)
    image.save("old-man.png")
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    image_bytes = buffered.getvalue()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    return image_base64


# ---------------------Other Routes----------------------------
Productsroute = APIRouter(prefix="/jholi-services/products", tags=["PRODUCTS"])


@Productsroute.get("/getProducts", status_code=status.HTTP_200_OK)
async def getProducts():
    try:
        return DatabaseModels.getAllProducts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=(e))


@Productsroute.get("/getProductCategories", status_code=status.HTTP_200_OK)
async def getProducts():
    try:
        return DatabaseModels.getProductCategories()
    except Exception as e:
        raise HTTPException(status_code=500, detail=(e))


# ----------------------Default-------------------------------
defualtroute = APIRouter(prefix="/jholi-backend/auth/defualt", tags=["Defualt"])


@defualtroute.post("/")
async def root():
    return """Welcome to JHOLI Server 1.10.1"""
