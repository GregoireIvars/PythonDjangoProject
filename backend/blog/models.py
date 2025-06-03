from django.db import models


def upload_to(instance, filename):
    """Fonction pour organiser le stockage des images"""
    return f'articles/{instance.titre[:20]}/{filename}'

class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    auteur = models.CharField(max_length=100)
    date_publication = models.DateTimeField(auto_now_add=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True, related_name="articles")
    images = models.ImageField(upload_to='articles/', null=True, blank=True)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-date_publication']
    

    def __str__(self):
        return self.titre

class Userprofile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Commentaire(models.Model):
    article = models.ForeignKey(Article, related_name='commentaires', on_delete=models.CASCADE)
    auteur = models.CharField(max_length=100)
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.auteur} on {self.article.titre}'


