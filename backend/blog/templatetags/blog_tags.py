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

@register.filter
def filter_by_language(articles, language_code):
    """Filtre les articles par langue"""
    if not language_code:
        return articles
    return articles.filter(langue=language_code)

@register.filter
def get_language_name(language_code):
    """Retourne le nom complet de la langue"""
    language_names = {
        'fr': 'Français',
        'en': 'English',
        'es': 'Español',
    }
    return language_names.get(language_code, language_code)

@register.filter
def get_language_flag(language_code):
    """Retourne le drapeau de la langue"""
    flags = {
        'fr': '🇫🇷',
        'en': '🇬🇧', 
        'es': '🇪🇸',
    }
    return flags.get(language_code, '🌐')