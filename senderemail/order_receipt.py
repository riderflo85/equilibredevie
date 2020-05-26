import os, requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, To, Content, Mail
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

    return str(response.status_code)

def sender_validation_cmd_client(order, user, another_adress):
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
            "products": []
        }
    }

    if another_adress:
        data['cmd']['anotheradress'] = {
            "ifyes": "true",
            "nameclient": f"{order.last_name.upper()} {order.first_name}",
            "adress": order.adress,
            "postalcode": str(order.postal_code),
            "city": order.city.upper(),
            "phonenumber": f"0{str(order.phone_number)}",
        }

    else:
        data['cmd']['anotheradress'] = {
            "ifyes": "false",
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

    url = "https://api.sendgrid.com/v3/mail/send"

    payload = {
        "personalizations": [{
            "to": [{
                "email": user.email,
                "name": str(user)
            }],
            "dynamic_template_data": data,
            "subject": "Validation de commande"
        }],
        "from": {
            "email": os.environ.get('FROM_EMAIL'),
            "name": os.environ.get('FROM_NAME_EMAIL')
        },
        "reply_to": {
            "email": os.environ.get('FROM_EMAIL'),
            "name": os.environ.get('FROM_NAME_EMAIL')
        },
        "template_id": "d-543faba5b6db4e45971c71f97f3fe243"
    }

    # payload = str(payload).replace("'", "\"")
    headers = {
        'authorization': f"Bearer {os.environ.get('SENDGRID_API_KEY')}",
        'content-type': "application/json; charset=utf8"
    }

    response = requests.post(url, data=payload, headers=headers)

    # import pdb; pdb.set_trace()
    return response.text
    # return str(payload)