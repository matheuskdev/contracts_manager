from django import forms

from . import models


class FolderForm(forms.ModelForm):

    class Meta:
        model = models.Folder
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "name": "Nome",
        }

    def __init__(self, *args, **kwargs):
        super(FolderForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.help_text:
                field.help_text = f"""
                                    <figcaption class="blockquote-footer">
                                    {field.help_text}
                                    </figcaption>
                                   """
