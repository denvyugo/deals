from django.forms import modelformset_factory
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from product.models import Deal
from product.forms import DealForm


def products(request):
    DealFormSet = modelformset_factory(Deal, form=DealForm, extra=1, can_delete=True)
    if request.method == 'POST':
        print(request.POST)
        formset = DealFormSet(request.POST, request.FILES)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for i, instance in enumerate(instances, 1):
                instance.save()

            return HttpResponseRedirect(reverse_lazy('products'))

    else:
        formset = DealFormSet(queryset=Deal.objects.all())
    return render(request, 'product/products.html', {'formset': formset})


def deals(request):
    DealFormSet = modelformset_factory(Deal, form=DealForm, extra=1)
    if request.method == 'POST':
        formset = DealFormSet(request.POST, request.FILES)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.save()

        return HttpResponseRedirect(reverse_lazy('deals'))
    else:
        formset = DealFormSet()
    return render(request, 'product/deals.html', {'formset': formset})
