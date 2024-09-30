from django import forms

from . import models


class AddendumForm(forms.ModelForm):

    class Meta:
        model = models.Addendum
        fields = [
            "title",
            "description",
            "effective_date",
            "new_end_date",
            "document",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "effective_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "new_end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "document": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "Titulo",
            "description": "Descrição",
            "effective_date": "Data",
            "contract": "Contrato",
            "new_end_date": "Nova Data Final",
            "document": "Arquivo",
        }

        def __init__(self, *args, **kwargs):
            super(AddendumForm, self).__init__(*args, **kwargs)
            for field in self.fields.values():
                if field.help_text:
                    field.help_text = f"""
                                        <figcaption class="blockquote-footer">
                                        {field.help_text}
                                        </figcaption>
                                    """
