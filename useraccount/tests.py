from django.test import TestCase, Client
from .models import User
from .forms import LoginForm, RegisterForm


class FormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'TestPseudoNoReplica',
            'supertester@tester.com',
            'testUserPassword!',
            first_name='TestFirstName',
            last_name='TestLastName',
            phone_number=1723456789,
            adress='134 Rue De Paris',
            postal_code=75000,
            city='Paris',
        )
        # self.user.save()

    def test_form_register(self):
        data = {
            'first_name': 'TestFirstName',
            'last_name': 'TestLastName',
            'username': 'TestPseudo',
            'email': 'test@tester.com',
            'password': 'testUserPassword!',
            'phone_number': 1723456789,
            'adress': '134 Rue De Paris',
            'postal_code': 75000,
            'city': 'Paris'
        }

        form = RegisterForm(data)
        is_valid = form.is_valid()
        user = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            phone_number=form.cleaned_data['phone_number'],
            adress=form.cleaned_data['adress'],
            postal_code=form.cleaned_data['postal_code'],
            city=form.cleaned_data['city'],
        )
        user.save()
        self.assertTrue(is_valid)
        self.assertEqual(User.objects.get(id=user.id).username, user.username)

    def test_form_login(self):
        data1 = {'email_or_id': self.user.username,
                'password': 'testUserPassword'}
        data2 = {'email_or_id': self.user.email,
                'password': 'testUserPassword'}

        self.assertTrue(LoginForm(data1).is_valid())
        self.assertTrue(LoginForm(data2).is_valid())


class UserActionTestCase(TestCase):
    def setUp(self):
        self.cli = Client()
        self.user = User.objects.create_user(
            'TestPseudoNoReplica',
            'supertester@tester.com',
            'testUserPassword!',
            first_name='TestFirstName',
            last_name='TestLastName',
            phone_number=1723456789,
            adress='134 Rue De Paris',
            postal_code=75000,
            city='Paris',
        )
    

    def test_login_whit_view(self):
        data = {'email_or_id': self.user.email,
                'password': 'testUserPassword!'}
        rep = self.cli.post('/user/login/', data)

        self.assertEqual(rep.status_code, 302)
