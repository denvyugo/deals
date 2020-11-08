from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

from datetime import datetime as dt


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


class DealLog(models.Model):
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='actions')
    timestamp = models.DateTimeField(blank=False)
    change = models.CharField(max_length=50, blank=False)
    value = models.CharField(max_length=255, blank=True)


def new_deal_log(deal, field, timestamp):
    DealLog.objects.create(deal=deal,
                           user=deal.user,
                           timestamp=timestamp,
                           change=field,
                           value=str(getattr(deal, field)))


def create_log(deal, field, timestamp, created):
    """create one log record"""
    if created:
        new_deal_log(deal=deal, field=field, timestamp=timestamp)
    else:
        # if value of field was changed then make log
        # get the latest log for field of corresponding deal
        log = DealLog.objects.filter(deal=deal, change=field).order_by('-timestamp').first()
        if log:
            if log.value != str(getattr(deal, field)):
                new_deal_log(deal=deal, field=field, timestamp=timestamp)
        else:
            new_deal_log(deal=deal, field=field, timestamp=timestamp)


def deal_changing_dispatcher(sender, instance, **kwargs):
    """log changes of deal: for each update field make a logging record"""
    timestamp = dt.now()
    create_log(deal=instance, field='customer', timestamp=timestamp, created=kwargs['created'])
    create_log(deal=instance, field='product', timestamp=timestamp, created=kwargs['created'])
    create_log(deal=instance, field='phone', timestamp=timestamp, created=kwargs['created'])
    create_log(deal=instance, field='resolution', timestamp=timestamp, created=kwargs['created'])
    create_log(deal=instance, field='comment', timestamp=timestamp, created=kwargs['created'])


post_save.connect(deal_changing_dispatcher, sender=Deal)
