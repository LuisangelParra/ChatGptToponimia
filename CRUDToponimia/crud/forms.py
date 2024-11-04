from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            "document_type",
            "document_id",
            "first_name",
            "second_name",
            "lasts_names",
            "birth_date",
            "gender",
            "email",
            "phone",
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        } 
