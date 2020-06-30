from django import forms


class CartAddProductForm(forms.Form):
    def __init__(self, *args, **kwargs):
        if 'declination' in kwargs.keys():
            choice_declination = kwargs.pop('declination')
            type_of_declination = kwargs.pop('declination_type')
        else:
            type_of_declination = None
            choice_declination = [('none', '------------')]

        super(CartAddProductForm, self).__init__(*args, **kwargs)
        self.fields['quantity'] = forms.IntegerField(
            min_value=1,
            max_value=300,
            initial=1,
            widget=forms.NumberInput(
                attrs={'class': 'quantity-input-choice'}
            )
        )
        self.fields['declination'] = forms.ChoiceField(
            label=type_of_declination,
            choices=choice_declination,
            required=False
        )
        self.fields['update'] = forms.BooleanField(
            required=False,
            initial=False,
            widget=forms.HiddenInput
        )


    # quantity = forms.IntegerField(
    #     min_value=1,
    #     max_value=300,
    #     initial=1,
    #     widget=forms.NumberInput(
    #         attrs={'class': 'quantity-input-choice'}
    #     )
    # )
    # declination = forms.ChoiceField(
    #     choices=choice_declination,
    #     required=False
    # )
    # update = forms.BooleanField(
    #     required=False,
    #     initial=False,
    #     widget=forms.HiddenInput
    # )
