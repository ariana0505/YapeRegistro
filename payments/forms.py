from django import forms
from django.utils import timezone

from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["customer_name", "amount", "paid_on"]
        widgets = {
            "customer_name": forms.TextInput(attrs={"autocomplete": "name", "placeholder": "Nombre del cliente"}),
            "amount": forms.NumberInput(attrs={"min": "0.01", "step": "0.01", "inputmode": "decimal", "placeholder": "0.00"}),
            "paid_on": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound and not self.instance.pk:
            self.initial["paid_on"] = timezone.localdate()

    def clean_customer_name(self):
        name = " ".join(self.cleaned_data["customer_name"].split())
        if not name:
            raise forms.ValidationError("Escribe el nombre del cliente.")
        return name


class PaymentFilterForm(forms.Form):
    name = forms.CharField(required=False, label="Nombre", max_length=120)
    day = forms.DateField(required=False, label="Fecha", widget=forms.DateInput(attrs={"type": "date"}))
