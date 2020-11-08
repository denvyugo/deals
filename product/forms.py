from django import forms
from product.models import Customer, Deal


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ()


class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.empty_permitted = False

    def clean(self):
        print('CLEAN CHECK')
        cleaned_data = super().clean()
        errors = []
        if 'product' not in cleaned_data:
            errors.append(forms.ValidationError('You should choose a product'))
        if 'phone' not in cleaned_data:
            errors.append(forms.ValidationError('You should add a phone'))
        if errors:
            print('THERE ARE ERRORS EXISTS!')
            raise forms.ValidationError(errors)

    def clean_phone(self):
        data = self.cleaned_data['phone']
        print('CHECK PHONE TO VALIDATE', data, data.isdigit(), len(data), type(data))
        if len(data) != 10 or not data.isdigit():
            print('Validation error!')
            raise forms.ValidationError('Phone field should consists of ten digits!')
        return data
