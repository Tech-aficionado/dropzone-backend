import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from services.otpGenerator import ManageOtp


class OtpVerificationMailingService:
    def __init__(self,mailAddress) -> int:
        userEmail = mailAddress
        
        otp = ManageOtp.otpGen()
        
        sender_email = "no.reply.todo2023@gmail.com"
        receiver_email = f"{userEmail}"
        password = "oqna rxbm taad liye"

        # Create the email content
        html_content = f"""
    <html>
      <body>
        <div style="background: #f3f2f0; height: 600px; width: 700px; border-radius: 0; padding: 20px;">
      <table style="width: 100%; background: #1b1b1f; border-top-left-radius: 0; border-top-right-radius: 0;">
        <tr>
          <td style="padding: 10px;">
            <h2 style="margin: 0; font-size: 24px; color: white;">DropZone</h2>
          </td>
          <td style="text-align: right; padding: 10px;">
            <span style="color: white; font-size: 16px;">Always Deliver Happiness</span>
          </td>
        </tr>
      </table>
      <div style="text-align: center; padding: 20px;">
        <h3 style="margin: 0;">Login || Register</h3>
        <p style="font-size: 16px; color: #333;">
          The email is intended to deliver a <strong>One-Time Password (OTP)</strong> to the user for authentication purposes during the login process. The OTP is a temporary code that enhances security by verifying the user's identity. The email should clearly state the purpose of the OTP, provide instructions on how to use it, and include any necessary security warnings.
        </p>
        <div style="background: white; width: 300px; margin: 0 auto; padding: 10px; font-size: 20px; border-radius: 0;">
          <strong>One-Time Password (OTP):</strong> <span style="font-weight: bold;">{otp}</span>
        </div>
          <div style=" width: 300px; margin: 0 auto; padding: 10px; font-size: 13px; border-radius: 0;">
          <p>This Otp is Valid for 3 Minutes... (180 seconds)</p>
        </div>
      </div>
    </div>
  </body>
</html>

"""
        subject = "OTP - DropZone"

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Add body to email
        message.attach(MIMEText(html_content, "html"))

        # Connect to the server and send the email
        try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()  # Secure the connection
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                print("Email sent successfully!")
        except Exception as e:
                print(f"Error: {e}")
        finally:
                server.quit()



