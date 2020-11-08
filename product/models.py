from django.db import models


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
    product = models.CharField(max_length=3, choices=PRODUCT_TYPE, blank=False)
    phone = models.CharField(max_length=10, blank=False)
    resolution = models.CharField(max_length=3, choices=RESOLUTION_TYPE, blank=True)
    comment = models.CharField(max_length=255, blank=True)
