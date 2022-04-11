from django import forms
from .models import PDFModel

class pdfForm(forms.ModelForm):
    class Meta:
        model= PDFModel
        fields= ['pdf']
