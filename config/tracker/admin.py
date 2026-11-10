from django.contrib import admin
from .models import Appliance


@admin.register(Appliance)
class ApplianceAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'brand',
        'owner',
        'purchase_date',
        'warranty_months',
    )

    search_fields = (
        'name',
        'brand',
        'model_number',
    )

    list_filter = (
        'category',
        'purchase_date',
    )