import logging
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import PaymentFilterForm, PaymentForm
from .models import Payment

logger = logging.getLogger(__name__)


def payment_list(request):
    if settings.DEMO_MODE:
        return demo_payment_list(request)
    return real_payment_list(request)


@login_required
def real_payment_list(request):
    filters = PaymentFilterForm(request.GET)
    payments = Payment.objects.all()
    filters_valid = filters.is_valid()
    day = filters.cleaned_data.get("day")
    if filters_valid:
        name = filters.cleaned_data["name"].strip()
        if name:
            payments = payments.filter(customer_name__icontains=name)
        if day:
            payments = payments.filter(paid_on=day)
    else:
        payments = Payment.objects.none()
    summary_day = day or timezone.localdate()
    summary = Payment.objects.filter(paid_on=summary_day).values("status").annotate(total=Sum("amount"))
    totals = {item["status"]: item["total"] for item in summary}
    return render(request, "payments/list.html", {
        "filters": filters,
        "filters_valid": filters_valid,
        "payments": payments,
        "summary_day": summary_day,
        "verified_total": totals.get(Payment.Status.VERIFIED, Decimal("0.00")),
        "pending_total": totals.get(Payment.Status.PENDING, Decimal("0.00")),
    })


def demo_payment_list(request):
    today = timezone.localdate()
    samples = [
        Payment(pk=1, customer_name="Ana Torres", amount=Decimal("12.50"), paid_on=today, status=Payment.Status.VERIFIED),
        Payment(pk=2, customer_name="Luis Ramos", amount=Decimal("28.00"), paid_on=today, status=Payment.Status.PENDING),
        Payment(pk=3, customer_name="María López", amount=Decimal("9.90"), paid_on=today, status=Payment.Status.VERIFIED),
        Payment(pk=4, customer_name="Carlos Díaz", amount=Decimal("18.40"), paid_on=today, status=Payment.Status.PENDING),
    ]
    filters = PaymentFilterForm(request.GET)
    filters_valid = filters.is_valid()
    day = filters.cleaned_data.get("day") if filters_valid else None
    summary_day = day or today
    totals = {
        status: sum(
            (payment.amount for payment in samples if payment.paid_on == summary_day and payment.status == status),
            Decimal("0.00"),
        )
        for status in Payment.Status.values
    }
    if filters_valid:
        name = filters.cleaned_data["name"].strip().casefold()
        payments = [
            payment for payment in samples
            if name in payment.customer_name.casefold() and (not day or payment.paid_on == day)
        ]
    else:
        payments = []
    return render(request, "payments/list.html", {
        "demo_mode": True,
        "filters": filters,
        "filters_valid": filters_valid,
        "payments": payments,
        "summary_day": summary_day,
        "verified_total": totals[Payment.Status.VERIFIED],
        "pending_total": totals[Payment.Status.PENDING],
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
def payment_set_status(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    desired_status = request.POST.get("status")
    if desired_status not in Payment.Status.values:
        return HttpResponseBadRequest("Estado de pago inválido.")
    payment = get_object_or_404(Payment, pk=pk)
    if payment.status != desired_status:
        payment.status = desired_status
        payment.save(update_fields=["status", "updated_at"])
        logger.info("payment_status_changed id=%s status=%s", payment.pk, payment.status)
        messages.success(request, "Estado del pago actualizado.")
    else:
        messages.info(request, "El pago ya tenía ese estado.")
    return redirect("payment-list")
