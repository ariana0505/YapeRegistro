from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "amount", "paid_on", "status", "created_at")
    list_filter = ("status", "paid_on")
    search_fields = ("customer_name",)
