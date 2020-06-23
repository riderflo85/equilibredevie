from decimal import Decimal
from django.conf import settings
from shop.models import Product, ShippingCosts


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products 
        from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def _get_product_shipping_costs(self, product, quantity):
        """
        Calculate the shipping costs on a product.
        """
        product_shipping_costs = 0
        for costs in ShippingCosts.objects.all():
            if costs.min_weight <= float(product.weight) and costs.max_weight >= float(product.weight):
                product_shipping_costs = float(costs.price)
        return product_shipping_costs * quantity

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_costs = self._get_product_shipping_costs(product, quantity)

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
                'costs': 0
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
            self.cart[product_id]['costs'] = product_costs
        else:
            self.cart[product_id]['quantity'] += quantity
            self.cart[product_id]['costs'] += product_costs

        self.save()

    def update(self, products_and_quantity):
        """
        Update the quantity of the product in the cart.
        """
        try:
            for i in products_and_quantity:
                data_cleaned = i.split(',')
                id_product = data_cleaned[0]
                quantity_product = data_cleaned[1]

                product = Product.objects.get(pk=int(id_product))

                self.cart[id_product]['quantity'] = int(quantity_product)
                self.cart[id_product]['costs'] = self._get_product_shipping_costs(
                    product, int(quantity_product))

            self.save()
            return True
        except:
            return False

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_shipping_costs(self):
        shipping_costs = 0.00
        for item in self.cart.values():
            shipping_costs += item['costs']

        return Decimal(str(shipping_costs)+"0")

    def get_total_price(self):
        without_shipping_costs = sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )
        with_shipping_costs = Decimal(self.get_shipping_costs()) + without_shipping_costs
        return [without_shipping_costs, with_shipping_costs]

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()



