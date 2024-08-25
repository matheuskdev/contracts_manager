from django import forms

from .models import Evaluation


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = [
            "rating",
            "comments",
        ]
        widgets = {
            "rating": forms.Select(attrs={"class": "form-control"}),
            "comments": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        labels = {
            "rating": "Nota",
            "comments": "Descrição",
            "contract": "Contrato",
        }

        def __init__(self, *args, **kwargs):
            super(EvaluationForm, self).__init__(*args, **kwargs)
            for field in self.fields.values():
                if field.help_text:
                    field.help_text = f"""
                                        <figcaption class="blockquote-footer">
                                        {field.help_text}
                                        </figcaption>
                                    """
