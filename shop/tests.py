from django.test import TestCase
from useraccount.models import User
from order.models import Order, OrderProductQuantity
from senderemail import order_receipt
from .models import Product, Category


class SendEmailTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'TestPseudoNoReplica',
            'supertester@tester.com',
            'testUserPassword!',
            civility='Mr',
            first_name='TestFirstName',
            last_name='TestLastName',
            phone_number=723456789,
            adress='134 Rue De Paris',
            postal_code=75000,
            city='Paris',
        )
        self.categ = Category.objects.create(
            name='categ test',
            slug='categ_test'
        )
        self.product = Product.objects.create(
            category = self.categ,
            name='test bicar',
            slug='test_bicar',
            price=12.22,
            available=True,
            priority='1',
        )
    
    def test_send_email_confirm_cmd(self):
        order = Order.objects.create(
            reference="18052020172922666298",
            last_name="Grenaille",
            first_name="Florent",
            adress="Route de la Bêchée",
            postal_code=85300,
            city="Challans",
            dep="vendée",
            phone_number=789651420,
            email="florent@gmail.com",
            url_receipt="https://url_de_recu_de_commande.com",
            total_price=12.22,
            note=' ',
            
        )