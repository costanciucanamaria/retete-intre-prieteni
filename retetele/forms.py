from django import forms
from .models import Retete, Comment

class ReteteForm(forms.ModelForm):
    class Meta:
        model = Retete
        fields = [
            'nume',
            "categorie",
            'ingrediente',
            'preparare',
            'timp_pregatire',
            'timp_gatire',
            'poza',
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]

