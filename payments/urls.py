from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
    path("", views.payment_list, name="payment-list"),
]
if not settings.DEMO_MODE:
    urlpatterns += [
        path("pagos/nuevo/", views.payment_create, name="payment-create"),
        path("pagos/<int:pk>/editar/", views.payment_edit, name="payment-edit"),
        path("pagos/<int:pk>/estado/", views.payment_set_status, name="payment-status"),
    ]
