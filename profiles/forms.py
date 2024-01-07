from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'user_full_name', 'user_email')

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        placeholders = {
            'user_contact_number': 'Contact Number',
            'user_address': 'Address',
            'user_postal_code': 'Post Code',
        }

        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False