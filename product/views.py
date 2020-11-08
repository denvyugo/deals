from django.forms import modelformset_factory
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from product.models import Customer, Deal
from product.forms import CustomerForm, DealForm


@login_required()
def products(request):
    DealFormSet = modelformset_factory(Deal, form=DealForm, extra=1)
    if request.method == 'POST':
        formset = DealFormSet(request.POST, request.FILES)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for i, instance in enumerate(instances, 1):
                instance.user = request.user
                instance.save()

            return HttpResponseRedirect(reverse_lazy('products'))

    else:
        formset = DealFormSet(queryset=Deal.objects.all())
    return render(request, 'product/products.html', {'formset': formset})


def customers(request):
    CustomerFormSet = modelformset_factory(Customer, form=CustomerForm, extra=1)
    if request.method == 'POST':
        formset = CustomerFormSet(request.POST, request.FILES)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.save()

        return HttpResponseRedirect(reverse_lazy('customers'))
    else:
        formset = CustomerFormSet()
    return render(request, 'product/customers.html', {'formset': formset})
