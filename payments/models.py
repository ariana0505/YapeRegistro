from django.core.validators import MinValueValidator
from django.db import models


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        VERIFIED = "verified", "Verificado"

    customer_name = models.CharField("cliente", max_length=120)
    amount = models.DecimalField("monto", max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    paid_on = models.DateField("fecha del pago")
    status = models.CharField("estado", max_length=8, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField("registrado el", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado el", auto_now=True)

    class Meta:
        ordering = ["-paid_on", "-created_at", "-id"]
        indexes = [models.Index(fields=["paid_on", "status"], name="payment_day_status_idx")]

    def __str__(self):
        return f"{self.customer_name} — S/ {self.amount} ({self.paid_on})"
