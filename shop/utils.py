from .models import Product


def filter_products_by_user_choice(filter_form):
    """
    Filter the all products in the database by the user choice
    """

    if filter_form.is_valid():
        user_choice = filter_form.cleaned_data['filter_choice']
        if user_choice != "none":
            products_filtered = Product.objects.all().order_by(user_choice)
            return products_filtered
        else:
            return "error"
    else:
        return "error"
