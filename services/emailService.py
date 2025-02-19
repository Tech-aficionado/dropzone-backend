import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from services.otpGenerator import ManageOtp


class OtpVerificationMailingService:
    def __init__(self, mailAddress) -> int:
        self.userEmail = mailAddress

    def sendOtp(self):
        otp = ManageOtp.otpGen(self.userEmail)

        sender_email = "no.reply.todo2023@gmail.com"
        receiver_email = f"{self.userEmail}"
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
          The email is intended to deliver a <strong>One-Time Password (OTP)</strong> to the user for authentication purposes during the login process but <stronger>if you fail to verify, your credentials will reset.</stronger> The OTP is a temporary code that enhances security by verifying the user's identity. The email should clearly state the purpose of the OTP, provide instructions on how to use it, and include any necessary security warnings.
        </p>
        <div style="background: white; width: 300px; margin: 0 auto; padding: 10px; font-size: 20px; border-radius: 0;">
          <strong>One-Time Password (OTP):</strong> <span style="font-weight: bold;">{otp}</span>
        </div>
          <div style=" width: 300px; margin: 0 auto; padding: 10px; font-size: 13px; border-radius: 0;">
          <p>This Otp is Valid for 3 Minutes... (180 seconds). </p>
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

    def onBoarding(self,Name):

        sender_email = "no.reply.todo2023@gmail.com"
        receiver_email = f"{self.userEmail}"
        password = "oqna rxbm taad liye"

        # Create the email content
        html_content = f"""
    <html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Our Company</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #f3f3f3;
            padding: 20px;
            text-align: center;
        }}
        .content {{
            padding: 20px;
        }}
        .button {{
            display: inline-block;
            padding: 10px 20px;
            background-color: #007bff;
            color: #ffffff;
            text-decoration: none;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to Our Company!</h1>
        </div>
        <div class="content">
            <p>Dear {Name},</p>
            <p>We're thrilled to have you on board. Here's what you can expect in the coming days:</p>
            <ul>
                <li>An introduction to our team</li>
                <li>Access to our tools and resources</li>
                <li>Your first project briefing</li>
            </ul>
            <p>To get started, please click the button below to set up your account:</p>
            <p><a href="#" class="button">Set Up Your Account</a></p>
            <p>If you have any questions, don't hesitate to reach out to our support team.</p>
            <p>Best regards,<br>DropZone</p>
        </div>
    </div>
</body>
</html>

"""  
        subject = "Welcome - DropZone"

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