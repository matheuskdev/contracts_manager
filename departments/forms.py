from django import forms

from . import models


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = models.Department
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "name": "Nome",
            "description": "Descrição",
            "created_at": "Criado em",
            "updated_at": "Atualizado em",
        }
