from time import sleep
from Database.database import DatabaseOperation
from Routes.Schemas import NewUserSchema
from fastapi import status


class DatabaseModels:
    def checkIfUserExists(Email: str):
        query = "SELECT * from USERS_TB WHERE EMAIL = %s"
        params = (Email,)

        result = DatabaseOperation.selectDB(query, params)
        if result.get("row") > 0:
            return dict(
                {"status": status.HTTP_302_FOUND, "details": result.get("detail")}
            )
        else:
            return status.HTTP_404_NOT_FOUND

    def checkIfUsernameExists(username: str):
        query = "SELECT * from USERS_TB WHERE USERNAME = %s"
        params = (username,)

        result = DatabaseOperation.selectDB(query, params)
        if result.get("row") > 0:
            return status.HTTP_208_ALREADY_REPORTED
        else:
            return status.HTTP_404_NOT_FOUND

    def checkIfEmailRegistered(email: str):
        query = "SELECT * from USERS_TB WHERE EMAIL = %s"
        params = (email,)

        result = DatabaseOperation.selectDB(query, params)
        if result is not None:
            if result.get("row") > 0:
                return status.HTTP_208_ALREADY_REPORTED
            else:
                return status.HTTP_404_NOT_FOUND
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    def createNewUser(userDetail: NewUserSchema):
        query = "INSERT INTO USERS_TB (USERNAME,FIRSTNAME,LASTNAME,EMAIL,PASS_X,AUTHYPE) VALUES (%s, %s,%s, %s,%s, %s)"
        params = (
            userDetail["USER_ID"],
            userDetail["F_NAME"],
            userDetail["L_NAME"],
            userDetail["EMAIL"],
            userDetail["PASSX"],
            userDetail["AUTHYPE"]
        )

        result = DatabaseOperation.CrudOperationsDB(query, params)
        if type(result) == dict and result.get("row") > 0:
            return result
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        

    def updateRefrshTokenUser(refresh_token: any, attempt: int, EMAIL: int):
        query = (
            "UPDATE USERS SET REFRESH_TOKEN = %s, REFRESH_ATTEMPT = %s WHERE EMAIL = %s"
        )
        params = (refresh_token, attempt, EMAIL)

        result = DatabaseOperation.CrudOperationsDB(query, params)
        if type(result) == dict and result.get("row") > 0:
            return result
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        
    def updateVerification(value: any,Email: any):
        query = (
            "UPDATE USERS_TB SET VERIFIED = %d where EMAIL = %s"
        )
        params = (value,Email)

        result = DatabaseOperation.CrudOperationsDB(query, params)
        if type(result) == dict and result.get("row") > 0:
            return result
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    def insertOtpRecord(otpCred: any):
        query = """INSERT INTO OTP_DIRECTORY (ID, TIME, OTP_VALUE)
VALUES (%s, %s, %s)
ON DUPLICATE KEY UPDATE
    TIME = VALUES(TIME),
    OTP_VALUE = VALUES(OTP_VALUE);"""
        params = (otpCred["id"], otpCred["TIME"], otpCred["OTP"])

        result = DatabaseOperation.CrudOperationsDB(query, params)
        if type(result) == dict and result.get("row") > 0:
            return result

        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    def checkOtpRecord(user_email: any):
        query = "SELECT * FROM  OTP_DIRECTORY WHERE ID = %s"
        params = (user_email,)

        result = DatabaseOperation.selectDB(query, params)
        if type(result) == dict and result.get("row") > 0:
            return result.get("detail")[0]
        if type(result) == dict and result.get("row") == 0:
            return status.HTTP_401_UNAUTHORIZED
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    def getAllProducts():
        query = """SELECT 
        p.ProductID,
        p.ProductName,
        p.Description,
        p.Reviews,
        p.StarCount,
        p.ImageRef,
        p.Price,
        b.BRAND_NAME AS BrandName,
        c.CategoryName AS CategoryName,
        d.list_name AS ListName
    FROM 
        products p
    INNER JOIN 
        brands b ON p.BrandID = b.BRAND_ID
    INNER JOIN 
        categories c ON p.CategoryID = c.CategoryID
    INNER JOIN 
        product_listing d ON p.ListID = d.list_id"""
        params = ()

        result = DatabaseOperation.selectDB(query, params)
        if result.get("row") > 0:
            return dict(
                {"status": status.HTTP_302_FOUND, "details": result.get("detail")}
            )
        else:
            return status.HTTP_404_NOT_FOUND

    def getProductCategories():
        query = "SELECT * from CATEGORIES"
        params = ()
        sleep(5)

        result = DatabaseOperation.selectDB(query, params)
        if result.get("row") > 0:
            return dict(
                {"status": status.HTTP_302_FOUND, "details": result.get("detail")}
            )
        else:
            return status.HTTP_404_NOT_FOUND
