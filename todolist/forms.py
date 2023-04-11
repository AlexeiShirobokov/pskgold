from django import forms
from .models import Request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'description', 'created_by', 'processed_by']
        widgets = {
            'created_by': forms.HiddenInput(),
            'processed_by': forms.HiddenInput(),
        }
