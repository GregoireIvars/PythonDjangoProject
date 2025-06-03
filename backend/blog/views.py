from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Article, Commentaire, Categorie, UserProfile
from .forms import ArticleForm, UserRegistrationForm, UserProfileForm

@login_required
@never_cache
def home(request):
    articles = Article.objects.all().order_by('-date_publication')
    return render(request, 'blog/home.html', {'articles': articles})

@login_required
@never_cache
def ajouter_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.auteur = request.user
            article.save()
            messages.success(request, 'Article ajouté avec succès !')
            return redirect('blog:detail_article', article_id=article.id)
    else:
        form = ArticleForm()
    
    return render(request, 'blog/ajouter_article.html', {'form': form})

@login_required
@never_cache
def modifier_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    if article.auteur != request.user:
        messages.error(request, "Vous n'avez pas l'autorisation de modifier cet article.")
        return redirect('blog:detail_article', article_id=article.id)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article modifié avec succès !')
            return redirect('blog:detail_article', article_id=article.id)
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'blog/modifier_article.html', {'form': form, 'article': article})

@login_required
@never_cache
def supprimer_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    if article.auteur != request.user:
        messages.error(request, "Vous n'avez pas l'autorisation de supprimer cet article.")
        return redirect('blog:detail_article', article_id=article.id)
    
    if request.method == 'POST':
        titre = article.titre
        article.delete()
        messages.success(request, f'Article "{titre}" supprimé avec succès.')
        return redirect('blog:home')
    
    return render(request, 'blog/confirmer_suppression.html', {'article': article})

@login_required
@never_cache
def detail_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    commentaires = article.commentaires.all().order_by('-date_publication')
    
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        if contenu and contenu.strip():
            Commentaire.objects.create(
                article=article,
                auteur=request.user,
                contenu=contenu.strip()
            )
            messages.success(request, "Commentaire ajouté avec succès.")
            return redirect('blog:detail_article', article_id=article.id)
        else:
            messages.error(request, "Le commentaire ne peut pas être vide.")
    
    context = {
        'article': article,
        'commentaires': commentaires,
        'peut_modifier': article.auteur == request.user,
    }
    return render(request, 'blog/detail_article.html', context)

# ✅ CORRECTION : Templates d'authentification dans auth/
@never_cache
def user_login(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
        
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} !')
            return redirect('blog:home')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    
    return render(request, 'auth/login.html')  # ✅ auth/ au lieu de blog/

@never_cache
def user_register(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Compte créé avec succès ! Vous pouvez maintenant vous connecter.')
            return redirect('blog:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/signup.html', {'form': form})  # ✅ signup.html !

@login_required
@never_cache
def user_logout(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('auth:login')  # Redirection vers login

# ✅ Templates de profil dans blog/
@login_required
@never_cache
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'auth/profile.html', {'profile': profile})

@login_required
@never_cache
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès !')
            return redirect('blog:profile')
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    
    return render(request, 'auth/edit_profile.html', {'form': form})