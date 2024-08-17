from django import forms

from . import models


class AddendumForm(forms.ModelForm):

    class Meta:
        model = models.Addendum
        fields = [
            "title",
            "description",
            "effective_date",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "effective_date": forms.DateInput( attrs={"class": "form-control", "type": "date"}),
        }
        labels = {
            "title": "Titulo",
            "description": "Descrição",
            "effective_date": "Data",
            "contract": "Contrato",
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
