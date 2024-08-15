from django import forms

from . import models


class HistoricalRecordForm(forms.ModelForm):

    class Meta:
        model = models.HistoricalRecord
        fields = ["content_type", "object_id", "owner"]
        widgets = {
            "content_type": forms.TextInput(attrs={"class": "form-control"}),
            "object_id": forms.TextInput(attrs={"class": "form-control"}),
            "change_date": forms.TextInput(attrs={"class": "form-control"}),
            "owner": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "content_type": "App",
            "object_id": "ID",
            "content_object": "APP-ID",
            "owner": "Criado por",
            "change_date": "Criado em",
            "change_type": "Atualizado em",
        }

    def __init__(self, *args, **kwargs):
        super(HistoricalRecordForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.help_text:
                field.help_text = f"""
                                    <figcaption class="blockquote-footer">
                                    {field.help_text}
                                    </figcaption>
                                   """
