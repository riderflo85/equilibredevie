from django import forms


class SearchProductForm(forms.Form):
    """
    Form for the user can search the product(s)
    """

    search_product = forms.CharField(
        label='Non du produit',
        max_length=200,
        widget=forms.TextInput(
            attrs={'placeholder': 'Trouver un produit...'}
        ),
    )
