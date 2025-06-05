from django import forms
from .models import Article, Categorie

class AIArticleGenerationForm(forms.Form):
    prompt = forms.CharField(
        label="Description de l'article",
        widget=forms.Textarea(attrs={
            'rows': 5,
            'class': 'form-control',
            'placeholder': 'Décrivez l\'article que vous souhaitez générer. Par exemple: "Un article sur les tendances technologiques en 2025, notamment l\'IA et son impact sur les métiers du numérique."'
        }),
        help_text="Soyez précis dans votre description pour obtenir un meilleur résultat."
    )
    
    titre = forms.CharField(
        label="Titre suggéré (optionnel)",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Laissez vide pour que l\'IA génère le titre'
        })
    )
    
    categorie = forms.ModelChoiceField(
        label="Catégorie",
        queryset=Categorie.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    langue = forms.ChoiceField(
        label="Langue",
        choices=Article.LANGUE_CHOICES,
        initial='fr',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    generer_image = forms.BooleanField(
        label="Générer une image pour l'article",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
