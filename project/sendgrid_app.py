import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail, To

from .config import FROM_EMAIL, SENDGRID_API_KEY


def send_email_sendgrid(recipient):
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    from_email = Email(FROM_EMAIL)
    to_email = To(recipient)  # Change to your recipient
    subject = "Sending with SendGrid is Fun"
    content = Content(
        "text/plain",
        """text/plain", "and easy to do anywhere,
                      even with Python""",
    )
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)
