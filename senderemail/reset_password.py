import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, To, Content, Mail, Personalization


def sender_reset_password(user, host):
    """
    Send the email to the user to reset his password.
    """
    link = f"{host}/user/reset_password/"
    data = {
        "code": user.check_code,
        "link": link,
        "username": str(user)
    }

    mail = Mail()
    mail.from_email = Email(
        os.environ.get('FROM_EMAIL'),
        os.environ.get('FROM_NAME_EMAIL')
    )
    mail.template_id = os.environ.get('ID_TEMPLATE_RESET_PASSWORD')
    mail.subject = "Réinitialisation de mot de passe."
    p = Personalization()
    p.add_to(Email(user.email, str(user)))
    p.dynamic_template_data = data
    mail.add_personalization(p)
    sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    response = sg.client.mail.send.post(request_body=mail.get())

    return response