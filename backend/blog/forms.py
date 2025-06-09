from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Article, Commentaire, Categorie, UserProfile

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'categorie', 'langue', 'images']
        widgets = {
            'titre': forms.TextInput(attrs={
                'placeholder': 'Titre de l\'article', 
                'class': 'form-control'
            }),
            'contenu': forms.Textarea(attrs={
                'rows': 8, 
                'placeholder': 'Rédigez votre article ici...', 
                'class': 'form-control'
            }),
            'categorie': forms.Select(attrs={
                'class': 'form-control'
            }),
            'langue': forms.Select(attrs={
                'class': 'form-control'
            }),
            'images': forms.FileInput(attrs={
                'class': 'form-control', 
                'accept': 'image/*'
            }),
        }

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Écrivez votre commentaire...',
                'class': 'form-control'
            })
        }

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={
                'placeholder': 'Nom de la catégorie',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Description (facultative)',
                'class': 'form-control'
            }),
        }

# ✅ Formulaire d'inscription modifié avec demande auteur
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Votre adresse email'
    }))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Votre prénom (facultatif)'
    }))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Votre nom (facultatif)'
    }))
    
    # ✅ Nouveaux champs pour demande auteur
    demander_auteur = forms.BooleanField(
        required=False,
        label="Je souhaite devenir auteur pour publier des articles",
        help_text="Votre demande sera examinée par un administrateur.",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    message_demande = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        required=False,
        label="Message de motivation (optionnel)",
        help_text="Expliquez pourquoi vous souhaitez devenir auteur."
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom d\'utilisateur'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmez le mot de passe'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
            # ✅ Gérer la demande d'auteur si cochée
            profile = user.profile
            if self.cleaned_data['demander_auteur']:
                profile.demande_auteur_statut = 'en_attente'
                profile.demande_auteur_date = timezone.now()
                profile.demande_auteur_message = self.cleaned_data['message_demande']
                profile.save()
        return user

# ✅ Nouveau formulaire pour demande auteur depuis profil
class DemandeAuteurForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        label="Message de motivation",
        help_text="Expliquez pourquoi vous souhaitez devenir auteur.",
        required=True
    )

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nom d\'utilisateur'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Prénom'
    }))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nom'
    }))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))

    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'date_naissance', 'ville', 'site_web']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Parlez-nous de vous...'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'date_naissance': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'ville': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre ville'
            }),
            'site_web': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://votre-site.com'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and hasattr(self.instance, 'user'):
            if User.objects.filter(email=email).exclude(pk=self.instance.user.pk).exists():
                raise forms.ValidationError("Cette adresse email est déjà utilisée par un autre utilisateur.")
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            user = profile.user
            user.first_name = self.cleaned_data.get('first_name', '')
            user.last_name = self.cleaned_data.get('last_name', '')
            user.email = self.cleaned_data.get('email', '')
            user.save()
            profile.save()
        return profile

class SimpleCommentForm(forms.Form):
    contenu = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Écrivez votre commentaire ici...',
            'required': True
        }),
        max_length=1000,
        help_text='Maximum 1000 caractères'
    )

    def clean_contenu(self):
        contenu = self.cleaned_data.get('contenu')
        if not contenu or not contenu.strip():
            raise forms.ValidationError("Le commentaire ne peut pas être vide.")
        return contenu.strip()