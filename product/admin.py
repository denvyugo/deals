import csv
from datetime import datetime as dt
from django.http import HttpResponse
from django.contrib import admin
from .models import Deal


def export_to_csv(modeladmin, request, queryset):
    """function to export data of model to cvs by triggered action"""
    objects = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;'\
                                      'filename={}.csv'.format(objects.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in objects.get_fields() if not field.many_to_many\
              and not field.one_to_many]
    # write header
    writer.writerow([field.name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, dt):
                value = dt.strftime(value, "%d/%m/%Y")
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['id', 'request_date', 'customer', 'product', 'resolution', 'user']
    actions = [export_to_csv]
