from django import forms
from .models import User


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
    confirm_password = forms.CharField(
        label='Confirmer votre mot de passe',
        max_length=128,
        min_length=8,
        required=True,
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = User
        fields = [
            'civility',
            'last_name',
            'first_name',
            'username',
            'email',
            'password',
            'confirm_password',
            'phone_number',
            'adress',
            'postal_code',
            'city',
        ]
        exclude = ['order']
