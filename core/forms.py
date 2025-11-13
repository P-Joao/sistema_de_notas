from django import forms
from .models import Avaliacao

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao  # Baseado no modelo Avaliacao
        
        # Inclui apenas os campos que o professor deve preencher
        fields = ['titulo', 'descricao', 'peso']
        
        # Adiciona widgets para melhorar a aparência
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'peso': forms.NumberInput(attrs={'step': '0.1', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deixa os campos com um visual mais "Bootstrap"
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})