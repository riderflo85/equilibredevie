import os, requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, To, Content, Mail, Personalization
from order.models import OrderProductQuantity


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

    return response

def sender_validation_cmd_client(order, user):
    """
    Send the email to the client for validate the order.
    """

    date_cmd = str(order.created).split(' ')[0].split('-')
    data = {
        "cmd": {
            "ref": order.reference,
            "nameclient": f"{user.last_name.upper()} {user.first_name}",
            "adress": user.adress,
            "postalcode": str(user.postal_code),
            "city": user.city.upper(),
            "phonenumber": f"0{str(user.phone_number)}",
            "anotheradress": {},
            "note": order.note,
            "date": f"{date_cmd[2]}/{date_cmd[1]}/{date_cmd[0]}",
            "totalprice": str(order.total_price),
            "shippingcosts": str(order.shipping_costs),
            "products": []
        }
    }

    if order.another_delivery_adress:
        data['cmd']['anotheradress'] = {
            "ifyes": True,
            "nameclient": f"{order.last_name.upper()} {order.first_name}",
            "adress": order.adress,
            "postalcode": str(order.postal_code),
            "city": order.city.upper(),
            "phonenumber": f"0{str(order.phone_number)}",
        }

    else:
        data['cmd']['anotheradress'] = {
            "ifyes": False,
            "nameclient": "none",
            "adress": "none",
            "postalcode": "none",
            "city": "none",
            "phonenumber": "none",
        }

    for product in OrderProductQuantity.objects.filter(id_order=order):
        data['cmd']['products'].append({
            "name": product.id_product.name,
            "priceunit": str(product.price),
            "totalprice": str(product.get_price()),
            "quantity": str(product.quantity)
        })

    mail = Mail()
    mail.from_email = Email(
        os.environ.get('FROM_EMAIL'),
        os.environ.get('FROM_NAME_EMAIL')
    )
    mail.template_id = os.environ.get('ID_TEMPLATE_VALID_CMD')
    mail.subject = "Validation de commande"
    p = Personalization()
    p.add_to(Email(user.email, str(user)))
    p.dynamic_template_data = data
    mail.add_personalization(p)
    sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    response = sg.client.mail.send.post(request_body=mail.get())

    return response
