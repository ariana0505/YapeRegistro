from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Payment


class PaymentFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="celia", password="test-only-password")

    def setUp(self):
        self.client.force_login(self.user)

    def test_create_then_verify_and_return_to_pending(self):
        response = self.client.post(reverse("payment-create"), {
            "customer_name": "  Ana   Torres  ", "amount": "12.50", "paid_on": "2026-10-14",
        })
        self.assertRedirects(response, reverse("payment-list"))
        payment = Payment.objects.get()
        self.assertEqual(payment.customer_name, "Ana Torres")
        self.assertEqual(payment.amount, Decimal("12.50"))
        self.assertEqual(payment.status, Payment.Status.PENDING)

        url = reverse("payment-toggle", args=[payment.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        self.client.post(url)
        payment.refresh_from_db()
        self.assertEqual(payment.status, Payment.Status.VERIFIED)
        self.client.post(url)
        payment.refresh_from_db()
        self.assertEqual(payment.status, Payment.Status.PENDING)

    def test_rejects_invalid_amount(self):
        response = self.client.post(reverse("payment-create"), {
            "customer_name": "Ana", "amount": "0", "paid_on": "2026-10-14",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Payment.objects.count(), 0)

    def test_accepts_minimum_amount(self):
        response = self.client.post(reverse("payment-create"), {
            "customer_name": "Ana", "amount": "0.01", "paid_on": "2026-10-14",
        })
        self.assertRedirects(response, reverse("payment-list"))
        self.assertEqual(Payment.objects.get().amount, Decimal("0.01"))

    def test_search_date_and_totals_do_not_mix_days_or_statuses(self):
        Payment.objects.create(customer_name="Ana", amount="10.10", paid_on=date(2026, 10, 14), status=Payment.Status.VERIFIED)
        Payment.objects.create(customer_name="ANA María", amount="5.20", paid_on=date(2026, 10, 14), status=Payment.Status.VERIFIED)
        Payment.objects.create(customer_name="Luis", amount="3.30", paid_on=date(2026, 10, 14))
        Payment.objects.create(customer_name="Ana", amount="99.00", paid_on=date(2026, 10, 13), status=Payment.Status.VERIFIED)

        response = self.client.get(reverse("payment-list"), {"name": "ana", "day": "2026-10-14"})
        self.assertEqual(len(response.context["payments"]), 2)
        self.assertEqual(response.context["verified_total"], Decimal("15.30"))
        self.assertEqual(response.context["pending_total"], Decimal("3.30"))

    def test_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("payment-list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_twenty_payments_remain_searchable_and_total_is_exact(self):
        day = date(2026, 10, 14)
        Payment.objects.bulk_create([
            Payment(customer_name=f"Cliente {number}", amount="1.25", paid_on=day, status=Payment.Status.VERIFIED)
            for number in range(20)
        ])
        response = self.client.get(reverse("payment-list"), {"name": "Cliente 19", "day": "2026-10-14"})
        self.assertEqual(len(response.context["payments"]), 1)
        self.assertEqual(response.context["verified_total"], Decimal("25.00"))
