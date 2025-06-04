from django import template

register = template.Library()

@register.filter
def has_role(user, role):
    """Vérifie si l'utilisateur a un rôle spécifique"""
    if not user.is_authenticated:
        return False
    try:
        return user.profile.role == role
    except:
        return False

@register.filter
def user_role(user):
    """Retourne le rôle de l'utilisateur"""
    if not user.is_authenticated:
        return 'visiteur'
    try:
        return user.profile.role
    except:
        return 'lecteur'

@register.filter
def can_create_articles(user):
    """Vérifie si l'utilisateur peut créer des articles"""
    if not user.is_authenticated:
        return False
    try:
        return user.profile.peut_creer_articles()
    except:
        return False

@register.filter
def can_request_author(user):
    """Vérifie si l'utilisateur peut demander à devenir auteur"""
    if not user.is_authenticated:
        return False
    try:
        return user.profile.peut_demander_auteur()
    except:
        return False

@register.filter
def can_manage_categories(user):
    """Vérifie si l'utilisateur peut gérer les catégories (admin uniquement)"""
    if not user.is_authenticated:
        return False
    try:
        return user.profile.peut_gerer_categories()
    except:
        return False