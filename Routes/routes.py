import json
from sqlalchemy import false
from Auth.authorize import authorize, verified_user
from Auth.authapikey import pwd_context
from Auth.jwt_token import create_access_jwt, create_refresh_jwt
from Database.Models import DatabaseModels
from Routes.Schemas import NewUserSchema, Phase1loginSchema, Phase2loginSchema, otpSchema
from fastapi import APIRouter, Depends, Request, status, HTTPException

from services.emailService import OtpVerificationMailingService
from services.otpGenerator import ManageOtp

# -----------------------Users--------------------------------
Usersroute = APIRouter(prefix="/jholi-services/users", tags=["USERS"])


@Usersroute.post("/newUser", status_code=status.HTTP_201_CREATED)
async def root(userdetails: NewUserSchema):
    try:
        userdetails.PASSX = pwd_context.hash(userdetails.PASSX)

        data = userdetails.model_dump()

        email_exist = DatabaseModels.checkIfUserExists(data["EMAIL"])
        if email_exist != 404:
            return HTTPException(
                status_code=status.HTTP_208_ALREADY_REPORTED,
                detail="User Already Exists",
            )
        user_obj = DatabaseModels.createNewUser(data)
        if user_obj["row"] > 0:
            return HTTPException(
                status_code=status.HTTP_200_OK, detail="User Created Successfully"
            )
        else:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something Went Wrong",
            )
    except Exception as e:
        raise HTTPException(
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

        checkes = pwd_context.verify(
            user.login_password, fetchedUser.get("details")[0].get("PASSX")
        )
        if not checkes:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password Didn't Match!!",
            )

        return {
            "message": "Phase 1 Successful",
            "status_code": status.HTTP_202_ACCEPTED
        }
    finally:
        pass


@Usersroute.post("/refreshToken")
async def refresh(token_data: dict = Depends(authorize)):
    return token_data

@Usersroute.post("/doctor")
async def getdoctor():
    return DatabaseModels.getdoctors()

@Usersroute.post("/activateOtp")
async def sendotp(user_email:otpSchema):
    email = user_email.user_email
    OtpVerificationMailingService(email)
    
    return {"message": "Otp Sent","statuscode":200}

@Usersroute.post("/phase2loginAuth")
async def sendotp(user:Phase2loginSchema):
    valid = ManageOtp.otpVerification(user.otp)
    if valid is False:
         return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Otp Not Verified",
            ) 

    data = {"email": user.user_email}
    access_token = create_access_jwt(data)

    refresh_token = create_refresh_jwt(data)
    store_refresh_token = DatabaseModels.updateRefrshTokenUser(
        refresh_token, 1, user.user_email
    )
    if store_refresh_token.get("row") == 0:
        return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Refresh Token Error!!",
        )

    return {
        "message": "Login Successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "type": "bearer",
        "status_code":status.HTTP_200_OK,
    }
    


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
