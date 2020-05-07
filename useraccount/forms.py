
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import User


# class LoginForm(AuthenticationForm):
#     """ Login form """

#     email = forms.CharField(
#         label='user',
#         max_length=100,
#         widget=forms.EmailInput(
#             attrs={'placeholder': 'Adresse email'}
#         ),
#     )
#     password = forms.CharField(
#         label='password',
#         widget=forms.PasswordInput(
#             attrs={'placeholder': 'Mot de passe'}
#         ),
#     )

class LoginForm(forms.Form):
    """ Login form """

    email_or_id = forms.CharField(
        label='email-or-id',
        max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': 'Adresse email ou identifiant'}
        ),
    )
    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Mot de passe'}
        ),
    )


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'phone_number',
            'adress',
            'postal_code',
            'city',
        ]
        exclude = ['order']