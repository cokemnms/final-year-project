from django import forms
from .models import Auction

class AuctionForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Auction
        fields = ['title', 'description', 'base_price', 'expires_at', 'images']
