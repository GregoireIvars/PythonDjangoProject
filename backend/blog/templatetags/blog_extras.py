from django import template
from ..models import UserProfile

register = template.Library()

@register.filter
def has_role(user, role):
    """Vérifie si l'utilisateur a un rôle spécifique"""
    if not user.is_authenticated:
        return False
    try:
        profile = UserProfile.objects.get(user=user)
        return profile.role == role
    except UserProfile.DoesNotExist:
        return False

@register.filter
def user_role(user):
    """Retourne le rôle de l'utilisateur"""
    if not user.is_authenticated:
        return 'visiteur'
    try:
        profile = UserProfile.objects.get(user=user)
        return profile.role
    except UserProfile.DoesNotExist:
        return 'lecteur'

@register.filter
def can_create_articles(user):
    """Vérifie si l'utilisateur peut créer des articles"""
    if not user.is_authenticated:
        return False
    try:
        profile = UserProfile.objects.get(user=user)
        return profile.peut_creer_articles()
    except UserProfile.DoesNotExist:
        return False

@register.filter
def can_request_author(user):
    """Vérifie si l'utilisateur peut demander à devenir auteur"""
    if not user.is_authenticated:
        return False
    try:
        profile = UserProfile.objects.get(user=user)
        return profile.peut_demander_auteur()
    except UserProfile.DoesNotExist:
        return True

@register.filter
def is_admin(user):
    """Vérifie si l'utilisateur est administrateur"""
    if not user.is_authenticated:
        return False
    try:
        profile = UserProfile.objects.get(user=user)
        return profile.role == 'admin'
    except UserProfile.DoesNotExist:
        return False

@register.filter
def is_author(user):
    """Vérifie si l'utilisateur est auteur"""
    if not user.is_authenticated:
        return False
    try:
        profile = UserProfile.objects.get(user=user)
        return profile.role in ['auteur', 'admin']
    except UserProfile.DoesNotExist:
        return False