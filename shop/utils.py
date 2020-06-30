from django.contrib.admin.utils import label_for_field
from .models import Category, ProductDeclination


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

def get_product_declination(product):
    """
    Get the all declination of the product.
    """

    declinations = ProductDeclination.objects.filter(original_product=product)
    choice_declination = [('none', ('-- Sélectionnez une déclinaison --'))]
    type_of_declination = ""

    for declination in declinations:
        choice_declination.append(
            (
                declination.declined_product.id,
                getattr(declination.declined_product,
                    declination.type_of_declination)
            )
        )
        if type_of_declination == "":
            type_of_declination = declination.type_of_declination
    
    type_of_declination = label_for_field(
        type_of_declination,
        product
    )
    
    return choice_declination, type_of_declination
