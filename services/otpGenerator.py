from oracledb import Time
from Database.Models import DatabaseModels
import datetime
import pyotp
totp = pyotp.TOTP('base32secret3232',interval=180)
class ManageOtp:
    def otpGen():
        otp = totp.now()
        now = datetime.datetime.now()
        params = dict()

        # DatabaseModels.insertOtpRecord()
        print(now)
        return otp
        

    def otpVerification(otp):
        return totp.verify(otp)
    