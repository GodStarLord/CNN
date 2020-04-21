from django import forms
from .models import Coins

class CoinsForm(forms.ModelForm):
    class Meta:
        model = Coins
        fields = ["coin_name", "full_name"]