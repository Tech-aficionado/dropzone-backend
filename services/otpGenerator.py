from Database.Models import DatabaseModels
from datetime import datetime, timedelta
import pyotp

totp = pyotp.TOTP("base32secret3232", interval=180, digits=4)


class ManageOtp:
    def otpGen(email: str):
        otp = totp.now()
        current_timestamp = datetime.now().timestamp()
        params = dict()
        params["OTP"] = int(otp)
        params["id"] = email
        params["TIME"] = current_timestamp
        DatabaseModels.insertOtpRecord(params)
        print(current_timestamp)
        print(otp)
        return otp

    def otpVerification(otp, email):
        response = DatabaseModels.checkOtpRecord(email)
        if response == 401 or response == 500 or response == [] or response == "":
            return False
        else:
            if datetime.now().timestamp() - response.get("time") < 180:
                if int(otp) == int(response.get("otp_value")):
                    return True
                else:
                    return False
            else:
                return False
