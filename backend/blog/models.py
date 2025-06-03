from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

def upload_to(instance, filename):
    """Fonction pour organiser le stockage des images"""
    return f'articles/{instance.titre[:20]}/{filename}'


def user_avatar_path(instance, filename):
    """Fonction pour organiser le stockage des avatars"""
    return f'avatars/{instance.user.username}/{filename}'


class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')  # Modifié pour utiliser User
    date_publication = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True, related_name="articles")
    images = models.ImageField(upload_to='articles/', null=True, blank=True)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-date_publication']
    
    def __str__(self):
        return self.titre

class UserProfile(models.Model):  # Renommé de Userprofile à UserProfile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, null=True)
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    site_web = models.URLField(blank=True)
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Profil de {self.user.username}"

    @property
    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/blog/images/default-avatar.png'

# Signal pour créer automatiquement un profil quand un utilisateur est créé
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

class Commentaire(models.Model):
    article = models.ForeignKey(Article, related_name='commentaires', on_delete=models.CASCADE)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentaires')  # Modifié pour utiliser User
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Commentaire de {self.auteur.username} sur {self.article.titre}'

    class Meta:
        ordering = ['-date_publication']


