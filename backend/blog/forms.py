from django import forms
from .models import Article, Commentaire, Categorie   # importe le modèle Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'auteur', 'categorie', 'images']  # Ajout du champ images
        widgets = {
            'titre': forms.TextInput(attrs={'placeholder': 'Titre de l\'article', 'class': 'form-control'}),
            'contenu': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Contenu', 'class': 'form-control'}),
            'auteur': forms.TextInput(attrs={'placeholder': 'Nom de l\'auteur', 'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'images': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
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