from django.db import models
from django.conf import settings


class Customer(models.Model):
    customer = models.CharField(max_length=120, blank=False)

    def __str__(self):
        return self.customer


class Deal(models.Model):
    AUTO = 'AUT'
    CONSUMER = 'CNS'
    SECURITY = 'SCR'
    MORTGAGE = 'MTG'
    PRODUCT_TYPE = [
        (AUTO, 'Автокредит'),
        (CONSUMER, 'Потребительский'),
        (SECURITY, 'Залог'),
        (MORTGAGE, 'Ипотека'),
    ]
    APPROVED = 'APR'
    REFUSAL = 'REF'
    HOLD = 'HLD'
    RESOLUTION_TYPE = [
        (APPROVED, 'Одобрено'),
        (REFUSAL, 'Отказ'),
        (HOLD, 'Временный отказ'),
    ]
    request_date = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.CharField(max_length=3, choices=PRODUCT_TYPE, blank=False)
    phone = models.CharField(max_length=10, blank=False)
    resolution = models.CharField(max_length=3, choices=RESOLUTION_TYPE, blank=True)
    comment = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='deals')
