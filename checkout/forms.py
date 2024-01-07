from django import forms
from .models import Order
from product.models import Variation  



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name',
            'email',
            'contact_number',
            'street_address',
            'postal_code',
            )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'contact_number': 'Contact Number',
            'street_address': 'Address',
            'postal_code': 'Post Code',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f"{placeholders[field]} *"
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False