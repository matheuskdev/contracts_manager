from django import forms
from . import models


class PartyForm(forms.ModelForm):

    class Meta:
        model = models.Party
        fields = ['name', 'address', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            
        }
        labels = {
            'name': 'Nome',
            'address': 'Endereço',
            'email': 'Email',
            'phone': 'Telefone',
            'created_at': 'Criado em',
            'updated_at':'Atualizado em',
        }