from django import forms

from .models import Rate


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ["currency_a", "currency_b"]
