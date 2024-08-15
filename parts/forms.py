from django import forms

from . import models


class PartForm(forms.ModelForm):

    class Meta:
        model = models.Part
        fields = ["name", "address", "email", "phone"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "name": "Nome",
            "address": "Endereço",
            "email": "Email",
            "phone": "Telefone",
            "created_at": "Criado em",
            "updated_at": "Atualizado em",
        }

    def __init__(self, *args, **kwargs):
        super(PartForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.help_text:
                field.help_text = f"""
                                    <figcaption class="blockquote-footer">
                                    {field.help_text}
                                    </figcaption>
                                   """
