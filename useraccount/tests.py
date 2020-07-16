from django.test import TestCase, Client
from django.contrib.auth.hashers import check_password
from senderemail.register import sender_activate_account
from senderemail.reset_password import sender_reset_password
from .models import User
from .forms import LoginForm, RegisterForm, ForgotPasswordForm


class FormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'TestPseudoNoReplica',
            'supertester@tester.com',
            'testUserPassword!',
            civility='Mr',
            first_name='TestFirstName',
            last_name='TestLastName',
            phone_number=1723456789,
            adress='134 Rue De Paris',
            postal_code=75000,
            city='Paris',
        )

    def test_form_register(self):
        data = {
            'civility': 'Mr',
            'first_name': 'TestFirstName',
            'last_name': 'TestLastName',
            'username': 'TestPseudo',
            'email': 'test@tester.com',
            'password': 'testUserPassword!',
            'confirm_password': 'testUserPassword!',
            'phone_number': 1723456789,
            'adress': '134 Rue De Paris',
            'postal_code': 75000,
            'city': 'Paris',
            'newsletter': True
        }

        form = RegisterForm(data)
        is_valid = form.is_valid()
        user = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            civility=form.cleaned_data['civility'],
            phone_number=form.cleaned_data['phone_number'],
            adress=form.cleaned_data['adress'],
            postal_code=form.cleaned_data['postal_code'],
            city=form.cleaned_data['city'],
            newsletter=form.cleaned_data['newsletter']
        )
        user.save()
        self.assertTrue(is_valid)
        self.assertEqual(User.objects.get(id=user.id).username, user.username)

    def test_sender_email_validate_account(self):
        self.user.generate_activate_key()
        rep = sender_activate_account(self.user, '127.0.0.1:8000')

        self.assertEqual(rep.status_code, 202)

    def test_form_login(self):
        data1 = {'email_or_id': self.user.username,
                'password': 'testUserPassword'}
        data2 = {'email_or_id': self.user.email,
                'password': 'testUserPassword'}

        self.assertTrue(LoginForm(data1).is_valid())
        self.assertTrue(LoginForm(data2).is_valid())

    def test_form_forgot_password(self):
        data = {
            'email': self.user.email,
            'phone_number': self.user.phone_number
        }
        form = ForgotPasswordForm(data)

        self.assertTrue(form.is_valid())


class UserActionTestCase(TestCase):
    def setUp(self):
        self.cli = Client()
        self.user = User.objects.create_user(
            'TestPseudoNoReplica',
            'supertester@tester.com',
            'testUserPassword!',
            civility='Mr',
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

    def test_register_with_view(self):
        data = {
            'civility': 'Mr',
            'first_name': 'TestFirstName',
            'last_name': 'TestLastName',
            'username': 'TestPseudo34',
            'email': 'test3434@tester.com',
            'password': 'testUserPassword!',
            'confirm_password': 'testUserPassword!',
            'phone_number': 1723456789,
            'adress': '134 Rue De Paris',
            'postal_code': 75000,
            'city': 'Paris'
        }

        rep = self.cli.post('/user/register/', data)

        self.assertEqual(rep.status_code, 302)

    def test_register_failed_duplicate_user_with_view(self):
        data = {
            'civility': 'Mr',
            'first_name': 'TestFirstName',
            'last_name': 'TestLastName',
            'username': 'TestPseudoNoReplica',
            'email': 'supertester@tester.com',
            'password': 'testUserPassword!',
            'confirm_password': 'testUserPassword!',
            'phone_number': 1723456789,
            'adress': '134 Rue De Paris',
            'postal_code': 75000,
            'city': 'Paris'
        }

        rep = self.cli.post('/user/register/', data)

        self.assertEqual(rep.context['error'], 'formulaire non valide')
        self.assertEqual(rep.status_code, 200)

    def test_register_failed_password_not_equal_with_view(self):
        data = {
            'civility': 'Mr',
            'first_name': 'TestFirstName',
            'last_name': 'TestLastName',
            'username': 'TestPseudoNo',
            'email': 'sutester@tester.com',
            'password': 'testUserPassword!',
            'confirm_password': 'notEqualtestUserPassword',
            'phone_number': 1723456789,
            'adress': '134 Rue De Paris',
            'postal_code': 75000,
            'city': 'Paris'
        }

        rep = self.cli.post('/user/register/', data)

        self.assertEqual(rep.context['error'], 'mot de passe non identique')
        self.assertEqual(rep.status_code, 200)

    def test_activate_user_account(self):
        self.user.generate_activate_key()
        rep = self.cli.get(
            f"/user/active_account?id={self.user.pk}&key={self.user.activate_key}"
        )

        self.assertEqual(rep.status_code, 200)
        self.assertTrue(rep.context['is_validate'])
        self.assertTrue(User.objects.get(pk=self.user.pk).is_verified)

    def test_fail_activate_user_account(self):
        self.user.generate_activate_key()
        rep = self.cli.get(f"/user/active_account?id={self.user.pk}&key=fail_key")

        self.assertEqual(rep.status_code, 200)
        self.assertFalse(rep.context['is_validate'])
        self.assertFalse(User.objects.get(pk=self.user.pk).is_verified)

    def test_forgot_user_password(self):
        data = {
            'email': self.user.email,
            'phone_number': self.user.phone_number
        }
        rep = self.cli.post('/user/forgot_password/', data)

        self.assertEqual(rep.status_code, 302)
        self.assertRedirects(rep, '/user/reset_password/')

    def test_fail_phone_number_forgot_user_password(self):
        data = {
            'email': self.user.email,
            'phone_number': 1122115444
        }
        rep = self.cli.post('/user/forgot_password/', data)

        self.assertEqual(rep.status_code, 200)
        self.assertEqual(
            rep.context['error'],
            "Numéro de téléphone non correspondant avec l'adresse email."
        )

    def test_fail_form_forgot_user_password(self):
        data = {
            'email': "unvalid.email?com",
            'phone_number': 114554788525
        }
        rep = self.cli.post('/user/forgot_password/', data)

        self.assertEqual(rep.status_code, 200)
        self.assertEqual(
            rep.context['error'],
            "Le formulaire n'est pas valide, merci de vérifier les champs."
        )

    def test_reset_user_password(self):
        self.user.generate_check_code_reset_password()
        
        data = {
            'code': self.user.check_code,
            'password': 'NewPasswordForReset',
            'confirm_password': 'NewPasswordForReset'
        }
        rep = self.cli.post('/user/reset_password/', data)

        self.assertEqual(rep.status_code, 302)
        self.assertRedirects(rep, '/user/success_reset_pwd/')

    def test_fail_reset_user_password(self):
        self.user.generate_check_code_reset_password()
        
        data = {
            'code': self.user.check_code,
            'password': 'NewPasswordForReset',
            'confirm_password': 'NewErrorPasswordForReset'
        }
        rep = self.cli.post('/user/reset_password/', data)

        self.assertEqual(rep.status_code, 200)
        self.assertEqual(rep.context['error'], 'Les mots de passe ne sont pas égaux.')

    def test_fail_form_reset_user_password(self):
        self.user.generate_check_code_reset_password()
        
        data = {
            'code': self.user.check_code,
            'password': 'pass',
            'confirm_password': 'pass'
        }
        rep = self.cli.post('/user/reset_password/', data)

        self.assertEqual(rep.status_code, 200)
        self.assertEqual(rep.context['error'], "Le formulaire n'est pas valide.")

    def test_fail_check_code_reset_user_password(self):
        self.user.generate_check_code_reset_password()
        
        data = {
            'code': 'fakeCode7',
            'password': 'NewPasswordForReset',
            'confirm_password': 'NewPasswordForReset'
        }
        rep = self.cli.post('/user/reset_password/', data)

        self.assertEqual(rep.status_code, 200)
        self.assertEqual(rep.context['error'], "Le code de vérification n'est pas valide.")

    def test_sender_reset_password(self):
        self.user.generate_check_code_reset_password()
        rep = sender_reset_password(self.user, "127.0.0.1:8000/user/reset_password/")

        self.assertEqual(rep.status_code, 202)


class ManageUserAccountTestCase(TestCase):
    def setUp(self):
        self.cli = Client()
        self.user = User.objects.create_user(
            'TestPseudoNo',
            'simpletester@tester.com',
            'testUserPassword!',
            civility='Mme',
            first_name='FNTestFirstName',
            last_name='LNTestLastName',
            phone_number=1723456789,
            adress='134 Rue De Paris',
            postal_code=75000,
            city='Paris',
        )
        self.cli.force_login(self.user)

    def test_change_user_password(self):
        rep1 = self.cli.get("/user/change_pwd/")
        self.assertEqual(rep1.status_code, 302)

        rep2 = self.cli.post("/user/change_pwd/", {
            "new_pwd": "myNewPassword"
        })

        user_new_pwd = User.objects.get(username=self.user.username).password
        check_pwd = check_password('myNewPassword', user_new_pwd)

        self.assertTrue(rep2.json()['success'])
        self.assertTrue(check_pwd)

    def test_fail_change_user_password(self):
        rep = self.cli.post("/user/change_pwd/", {
            "new_fail": "fail"
        })

        self.assertFalse(rep.json()['success'])
