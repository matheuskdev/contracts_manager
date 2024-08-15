from django import forms

from . import models


class ContractForm(forms.ModelForm):

    class Meta:
        model = models.Contract
        exclude = ["email_enviado"]
        fields = [
            "number",
            "subject",
            "description",
            "amount",
            "pdf",
            "start_date",
            "end_date",
            "active",
            "lgpd",
            "automatic_renewal",
            "contains_addendum",
            "parts",
            "folder",
            "department",
        ]
        widgets = {
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "pdf": forms.FileInput(
                attrs={
                    "class": "custom-file-input",
                    "type": "file",
                    "autofocus": "autofocus",
                }
            ),
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "lgpd": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "automatic_renewal": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "contains_addendum": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "parts": forms.SelectMultiple(attrs={"class": "form-control"}),
            "folder": forms.Select(attrs={"class": "form-control"}),
            "department": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "number": "Número",
            "subject": "Assunto",
            "description": "Descrição",
            "amount": "Valor",
            "pdf": "Arquivo PDF",
            "start_date": "Data de Início",
            "end_date": "Data de Término",
            "active": "Ativo",
            "lgpd": "Conformidade LGPD",
            "automatic_renewal": "Renovação Automática",
            "contains_addendum": "Contém Aditivo",
            "parts": "Partes Envolvidas",
            "folder": "Pasta",
            "department": "Setor",
        }

    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.help_text:
                field.help_text = f"""
                                    <figcaption class="blockquote-footer">
                                    {field.help_text}
                                    </figcaption>
                                   """
