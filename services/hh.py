import smtplib

def verify_email_smtp(email_address):
    try:
        # Connect to the mail server
        server = smtplib.SMTP('smtp.sendgrid.net', 587)
        server.set_debuglevel(1)  # Show communication with the server
        server.starttls()  # Secure the connection
        server.ehlo()

        # Attempt to verify the email address
        response_code, _ = server.verify(email_address)
        return response_code == 250
    except smtplib.SMTPServerDisconnected:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        server.quit()

# Example usage
email = "agsgxharmony@gmail.com"
is_valid = verify_email_smtp(email)
print(f"Email is valid: {is_valid}")