import os, requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, To, Content, Mail


def sender_receipt(order, user):
    """
    Send the order receipt to the client.
    """

    # Retrieves the HTML page that contains the client order receipt.
    # (Order reciept make by Stripe.com)
    r = requests.get(order.url_receipt)

    sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(
        os.environ.get('FROM_EMAIL'),
        os.environ.get('FROM_NAME_EMAIL')
    )
    to_email = To(user.email, str(user))
    subject = "Reçu de commande"
    content = Content("text/html", r.text)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    return str(response.status_code)
