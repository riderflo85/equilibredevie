def create_stripe_client(stripe_obj, user, dep):
    """
    Create the new client in stripe dashboard
    """

    new_customer = stripe_obj.Customer.create(
        address={
            'line1': user.adress,
            'city': user.city,
            'postal_code': user.postal_code,
            'state': dep,
        },
        email=user.email,
        name=str(user),
        phone=f"0{str(user.phone_number)}"
    )

    return new_customer['id']

def check_stripe_client(stripe_obj, user, dep):
    """
    Check if the current authenticated user exist in the stripe dashboarb.
    """

    all_customers = stripe_obj.Customer.list()
    match_customer_id = False

    for customer in all_customers['data']:
        if customer['email'] == user.email:
            match_customer_id = customer['id']
            break
        else:
            pass
    
    if match_customer_id == False:
        return create_stripe_client(stripe_obj, user, dep)
    else:
        return match_customer_id