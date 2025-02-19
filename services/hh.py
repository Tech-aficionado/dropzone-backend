
import smtplib
import sys
 
CARRIERS = {
    "airtel": "@airtelap.com",
    "idea": "@ideacellular.net",
    "vodafone": "@vodafone.net",
    "bsnl": "@bsnl.in"
}
 
EMAIL = "no.reply.todo2023@gmail.com"
PASSWORD = "oqna rxbm taad liye"
 
def send_message(phone_number, carrier, message):
    recipient = phone_number + CARRIERS[carrier]
    auth = (EMAIL, PASSWORD)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(auth[0], auth[1])
        server.sendmail(auth[0], recipient, message)
        print("Message sent successfully")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        server.quit()
 
 
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(f"Usage: python3 {sys.argv[0]} <PHONE_NUMBER> <CARRIER> <MESSAGE>")
        sys.exit(0)
 
    phone_number = sys.argv[1]
    carrier = sys.argv[2]
    message = sys.argv[3]
 
    send_message(phone_number, carrier, message)