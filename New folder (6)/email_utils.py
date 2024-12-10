from aiosmtplib import send
from email.message import EmailMessage

async def send_activation_email(email, user_id):
    activation_link = f"http://localhost:8000/activate/{user_id}"
    message = EmailMessage()
    message["From"] = "your_email@example.com"
    message["To"] = email
    message["Subject"] = "Activate Your Account"
    message.set_content(
        f"Hi! Thank you for signing up. Click this link to activate your account: {activation_link}"
    )

    await send(message, hostname="smtp.gmail.com", port=587, start_tls=True,
               username="your_email@example.com", password="your_password")
