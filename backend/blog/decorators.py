from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def require_role(required_roles):
    """Décorateur pour vérifier les rôles utilisateur"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Connectez-vous pour accéder à cette page.")
                return redirect('blog:login')
            
            try:
                user_role = request.user.profile.role
            except:
                user_role = 'lecteur'
            
            if user_role not in required_roles:
                messages.error(request, "Vous n'avez pas les permissions pour accéder à cette page.")
                return redirect('blog:home')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def require_author(view_func):
    """Décorateur pour les fonctionnalités auteur"""
    return require_role(['auteur', 'admin'])(view_func)

def require_admin(view_func):
    """Décorateur pour les fonctionnalités admin"""
    return require_role(['admin'])(view_func)

def require_article_owner_or_admin(view_func):
    """Décorateur pour vérifier propriétaire d'article ou admin"""
    @wraps(view_func)
    def wrapper(request, article_id, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Connectez-vous pour accéder à cette page.")
            return redirect('blog:login')
        
        from .models import Article
        from django.shortcuts import get_object_or_404
        
        article = get_object_or_404(Article, id=article_id)
        try:
            user_role = request.user.profile.role
        except:
            user_role = 'lecteur'
        
        if article.auteur != request.user and user_role != 'admin':
            messages.error(request, "Vous ne pouvez modifier que vos propres articles.")
            return redirect('blog:detail_article', article_id=article.id)
        
        return view_func(request, article_id, *args, **kwargs)
    return wrapper