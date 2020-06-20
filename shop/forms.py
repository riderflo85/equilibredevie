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


class FilterProductForm(forms.Form):
    """
    Form for the user can filter the product(s)
    """

    choices_filter = [
        ('none', '----------'),
        ('name', 'A à Z'),
        ('-name', 'Z à A'),
        ('-price', 'Prix ++'),
        ('price', 'Prix --')
    ]

    filter_choice = forms.ChoiceField(
        label='Trier par',
        choices=choices_filter,
    )