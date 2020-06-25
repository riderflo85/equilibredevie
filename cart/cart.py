from decimal import Decimal
from django.conf import settings
from django.db.models import Q
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
        self.weight = 0

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

    def _get_product_weight(self, product, quantity):
        """
        Get the total weight of the product.
        """
        total_weight = product.weight * quantity
        return total_weight

    def _get_total_shipping_costs(self, weight):
        """
        Get the shipping costs of the cart.
        """
        costs = 0
        try:
            costs = ShippingCosts.objects.get(
                Q(min_weight__lte=weight),
                Q(max_weight__gte=weight)
            ).price
        except:
            costs = 0

        return costs

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        total_weight = self._get_product_weight(product, quantity)
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
                'weight': 0,
                'costs': 0
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
            self.cart[product_id]['weight'] = total_weight
        else:
            self.cart[product_id]['quantity'] += quantity
            self.cart[product_id]['weight'] += total_weight

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
                self.cart[id_product]['weight'] = self._get_product_weight(
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

    def get_total_cart_weight(self):
        """
        Get the total weight of the cart.
        """
        total_weight = 0
        for item in self.cart.values():
            total_weight += item['weight']
        
        return total_weight

    def get_shipping_costs(self):
        """
        Get the shipping costs of the cart.
        """
        total_weight = self.get_total_cart_weight()
        shipping_costs = self._get_total_shipping_costs(total_weight)

        return Decimal(str(shipping_costs))

    def get_total_price(self):
        """
        Get the total price with the shipping costs
        and without the shipping costs.
        """
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
