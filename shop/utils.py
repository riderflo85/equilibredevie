from .models import Category


def filter_products_by_user_choice(filter_form, products):
    """
    Filter the all products in the database by the user choice.
    """

    if filter_form.is_valid():
        user_choice = filter_form.cleaned_data['filter_choice']
        if user_choice != "none":
            products_filtered = products.order_by(user_choice)
            return products_filtered
        else:
            return "error"
    else:
        return "error"

def filter_products_by_categories(filter_categ):
    """
    Filter the all products in the database by the product categories.
    """

    category = Category.objects.get(slug=filter_categ)
    products = category.products.all()

    if len(products) > 0:
        return products
    else:
        return "error"
