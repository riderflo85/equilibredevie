import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, To, Content, Mail, Personalization


def sender_activate_account(user, host):
    """
    Send the email to the user to active his account.
    """
    link = f"{host}/user/active_account?id={user.pk}&key={user.activate_key}"
    data = {"username": str(user), "link": link}

    mail = Mail()
    mail.from_email = Email(
        os.environ.get('FROM_EMAIL'),
        os.environ.get('FROM_NAME_EMAIL')
    )
    mail.template_id = os.environ.get('ID_TEMPLATE_ACTIVE_ACCOUNT')
    mail.subject = "Activation de compte client"
    p = Personalization()
    p.add_to(Email(user.email, str(user)))
    p.dynamic_template_data = data
    mail.add_personalization(p)
    sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    response = sg.client.mail.send.post(request_body=mail.get())

    return response