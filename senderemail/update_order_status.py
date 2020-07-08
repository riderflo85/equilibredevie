import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, To, Content, Mail, Personalization


def sender_new_order_status(order_queryset):
    """
    Sending an email to the client to indicate a change of status.
    """

    done = True

    for order in order_queryset:

        data = {
            'reforder': order.reference,
            'clientname': order.first_name,
            'price': order.total_price,
            'status': order.status
        }

        mail = Mail()
        mail.from_email = Email(
            os.environ.get('FROM_EMAIL'),
            os.environ.get('FROM_NAME_EMAIL')
        )
        mail.template_id = os.environ.get('ID_TEMPLATE_UPDATE_CMD')
        mail.subject = "Le statu de votre commande a changée"
        p = Personalization()
        p.add_to(Email(
            order.email,
            f"{order.last_name} {order.first_name}"
        ))
        p.dynamic_template_data = data
        mail.add_personalization(p)
        sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        response = sg.client.mail.send.post(request_body=mail.get())

        if response.status_code == 202:
            continue
        else:
            done = False

    return done
