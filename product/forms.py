from django import forms
from product.models import Deal


class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.empty_permitted = False

    def clean(self):
        print('CLEAN CHECK')
        cleaned_data = super().clean()
        errors = []
        # for data in cleaned_data:
        #     print(type(data), data)
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

    def form_valid(self, form):
        print('IF FORM VALID WE SHOULD DO SOMETHING WITH DATA')
        # context = self.get_context_data()
        # orderitems = context['orderitems']
        #
        # with transaction.atomic():
        #     self.object = form.save()
        #     if orderitems.is_valid():
        #         orderitems.instance = self.object
        #         orderitems.save()
        #
        # # удаляем пустой заказ
        # if self.object.get_total_cost() == 0:
        #     self.object.delete()

        return super().form_valid(form)
