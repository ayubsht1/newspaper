from django import forms
from newspaper.models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        models = Contact
        fields = '__all__'