from Database.database import DatabaseOperation
from Routes.Schemas import NewUserSchema
from fastapi import status


class DatabaseModels:
    def checkIfUserExists(Email: str):
        query = "SELECT * from USERS WHERE EMAIL = %s"
        params = (Email,)

        result = DatabaseOperation.selectDB(query, params)
        if result.get("row") > 0:
            return dict(
                {"status": status.HTTP_302_FOUND, "details": result.get("detail")}
            )
        else:
            return status.HTTP_404_NOT_FOUND

    def createNewUser(userDetail: NewUserSchema):
        query = "INSERT INTO USERS (USER_ID,F_NAME,EMAIL,PASSX) VALUES (%s, %s,%s, %s)"
        params = (
            userDetail["USER_ID"],
            userDetail["F_NAME"],
            userDetail["EMAIL"],
            userDetail["PASSX"],
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
        

    def insertOtpRecord(userDetail: any):
        query = "INSERT INTO OTP_DIRECTORY (ID,TIME,OTP) VALUES (%s,%s,%s)"
        params = (
            '',
            userDetail["TIME"],
            userDetail["OTP"]
        )

        result = DatabaseOperation.CrudOperationsDB(query, params)
        if type(result) == dict and result.get("row") > 0:
            return result
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        
    def getAllProducts():
        query = "SELECT * from PRODUCTS"
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

        result = DatabaseOperation.selectDB(query, params)
        if result.get("row") > 0:
            return dict(
                {"status": status.HTTP_302_FOUND, "details": result.get("detail")}
            )
        else:
            return status.HTTP_404_NOT_FOUND
        
