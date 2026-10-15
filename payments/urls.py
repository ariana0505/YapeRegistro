from django.urls import path

from . import views

urlpatterns = [
    path("", views.payment_list, name="payment-list"),
    path("pagos/nuevo/", views.payment_create, name="payment-create"),
    path("pagos/<int:pk>/editar/", views.payment_edit, name="payment-edit"),
    path("pagos/<int:pk>/estado/", views.payment_toggle, name="payment-toggle"),
]
