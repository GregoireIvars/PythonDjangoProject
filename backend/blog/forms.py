from django import forms
from .models import Article, Commentaire, Categorie   # importe le modèle Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'auteur', 'categorie']
        widgets = {
            'titre': forms.TextInput(attrs={'placeholder': 'Titre de l\'article'}),
            'contenu': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Contenu'}),
            'auteur': forms.TextInput(attrs={'placeholder': 'Nom de l\'auteur'}),
            'categorie': forms.Select(), # Remplace TextInput par Select
        }

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['auteur', 'contenu']

# Ajoutez cette classe dans forms.py
class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Nom de la catégorie'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Description (facultative)'}),
        }