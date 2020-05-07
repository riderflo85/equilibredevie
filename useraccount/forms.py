
from django.contrib.auth.forms import AuthenticationForm
from django import forms


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