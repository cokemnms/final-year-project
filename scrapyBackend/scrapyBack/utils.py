import sendgrid
from sendgrid.helpers.mail import Mail
from django.conf import settings

def send_reset_email(user, token):
    reset_url = f"http://localhost:3000/reset-password/{user.pk}/{token}"  # Vue route
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=user.email,
        subject="Password Reset Request",
        html_content=f"""
            <p>Hi {user.firstName},</p>
            <p>Click the link below to reset your password:</p>
            <a href="{reset_url}">Reset Password</a>
            <p>This link will expire soon.</p>
        """
    )
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    sg.send(message)
