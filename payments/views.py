import logging
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import PaymentFilterForm, PaymentForm
from .models import Payment

logger = logging.getLogger(__name__)


@login_required
def payment_list(request):
    filters = PaymentFilterForm(request.GET)
    payments = Payment.objects.all()
    if filters.is_valid():
        name = filters.cleaned_data["name"].strip()
        day = filters.cleaned_data["day"]
        if name:
            payments = payments.filter(customer_name__icontains=name)
        if day:
            payments = payments.filter(paid_on=day)
    else:
        day = None
    summary_day = day or timezone.localdate()
    summary = Payment.objects.filter(paid_on=summary_day).values("status").annotate(total=Sum("amount"))
    totals = {item["status"]: item["total"] for item in summary}
    return render(request, "payments/list.html", {
        "filters": filters,
        "payments": payments,
        "summary_day": summary_day,
        "verified_total": totals.get(Payment.Status.VERIFIED, Decimal("0.00")),
        "pending_total": totals.get(Payment.Status.PENDING, Decimal("0.00")),
    })


@login_required
def payment_create(request):
    form = PaymentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        payment = form.save()
        logger.info("payment_created id=%s", payment.pk)
        messages.success(request, "Pago registrado como pendiente.")
        return redirect("payment-list")
    return render(request, "payments/form.html", {"form": form, "title": "Registrar pago", "submit_label": "Guardar pago"})


@login_required
def payment_edit(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    form = PaymentForm(request.POST or None, instance=payment)
    if request.method == "POST" and form.is_valid():
        form.save()
        logger.info("payment_edited id=%s", payment.pk)
        messages.success(request, "Pago actualizado.")
        return redirect("payment-list")
    return render(request, "payments/form.html", {"form": form, "title": "Corregir pago", "submit_label": "Guardar cambios"})


@login_required
def payment_toggle(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    payment = get_object_or_404(Payment, pk=pk)
    payment.status = Payment.Status.PENDING if payment.status == Payment.Status.VERIFIED else Payment.Status.VERIFIED
    payment.save(update_fields=["status", "updated_at"])
    logger.info("payment_status_changed id=%s status=%s", payment.pk, payment.status)
    messages.success(request, "Estado del pago actualizado.")
    return redirect("payment-list")
