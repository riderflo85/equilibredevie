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


class ForgotPasswordForm(forms.Form):
    """
    Forgot password
    """

    email = forms.EmailField(
        label='email',
        widget=forms.EmailInput(
            attrs={"placeholder": 'Adresse email valide.'}
        ),
    )
    phone_number = forms.IntegerField(
        label='Numéro de téléphone',
        max_value=9999999999,
        widget=forms.NumberInput(
            attrs={"placeholder": "Numéro de téléphone utilisé lors de l'inscription."}
        ),
    )


class ResetPasswordForm(forms.Form):
    """
    Reset the user password
    """

    code = forms.CharField(
        label='code',
        max_length=10,
        widget=forms.TextInput(
            attrs={"placeholder": "Code reçu par email."}
        )
    )
    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Nouveau mot de passe.'}
        ),
    )
    confirm_password = forms.CharField(
        label='Confirmer votre mot de passe',
        max_length=128,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirmer votre mote de passe."}
        ),
    )
