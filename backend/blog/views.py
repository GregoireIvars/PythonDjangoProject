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

# ✅ HOME - Accessible à tous
@never_cache
def home(request):
    articles = Article.objects.all().order_by('-date_publication')
    total_articles = articles.count()
    total_users = User.objects.count()
    
    context = {
        'articles': articles,
        'total_articles': total_articles,
        'total_users': total_users,
        'is_public_view': not request.user.is_authenticated,
    }
    return render(request, 'blog/home.html', context)

# ✅ DETAIL ARTICLE - Accessible à tous, redirection seulement pour commentaires
@never_cache
def detail_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    commentaires = article.commentaires.all().order_by('-date_publication')
    
    # ✅ Commentaires uniquement pour les utilisateurs connectés
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.info(request, "Connectez-vous pour pouvoir commenter cet article.")
            # ✅ Utilise le nom d'URL au lieu du chemin direct
            return redirect('blog:login')  # Au lieu de f"/login/?next={request.path}"
        
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
        'peut_modifier': request.user.is_authenticated and article.auteur == request.user,
        'peut_commenter': request.user.is_authenticated,
    }
    return render(request, 'blog/detail_article.html', context)

# ✅ CREATION ARTICLE - Redirection custom si pas connecté
@never_cache
def ajouter_article(request):
    # ✅ Redirection custom au lieu de @login_required
    if not request.user.is_authenticated:
        messages.info(request, "Connectez-vous pour créer un article.")
        return redirect('blog:login')
    
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

# ✅ MODIFICATION ARTICLE - Redirection custom si pas connecté
@never_cache
def modifier_article(request, article_id):
    if not request.user.is_authenticated:
        messages.info(request, "Connectez-vous pour modifier cet article.")
        return redirect('blog:login')
    
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

# ✅ SUPPRESSION ARTICLE - Redirection custom si pas connecté
@never_cache
def supprimer_article(request, article_id):
    if not request.user.is_authenticated:
        messages.info(request, "Connectez-vous pour supprimer cet article.")
        return redirect('blog:login')
    
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

# ✅ AUTHENTIFICATION
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
            
            # ✅ Redirection intelligente
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('blog:home')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    
    return render(request, 'auth/login.html')

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
    
    return render(request, 'auth/signup.html', {'form': form})

# ✅ LOGOUT - Garde @login_required pour sécurité
@login_required
@never_cache
def user_logout(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('blog:home')

# ✅ PROFIL - Redirection custom si pas connecté
@never_cache
def profile(request):
    if not request.user.is_authenticated:
        messages.info(request, "Connectez-vous pour accéder à votre profil.")
        return redirect('blog:login')
    
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'auth/profile.html', {'profile': profile})

# ✅ EDIT PROFIL - Redirection custom si pas connecté
@never_cache
def edit_profile(request):
    if not request.user.is_authenticated:
        messages.info(request, "Connectez-vous pour modifier votre profil.")
        return redirect('blog:login')
    
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

# ✅ Vues pour catégories - Accessibles à tous
@never_cache
def liste_categories(request):
    categories = Categorie.objects.all()
    return render(request, 'blog/liste_categories.html', {'categories': categories})

@never_cache
def articles_par_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    articles = Article.objects.filter(categorie=categorie).order_by('-date_publication')
    return render(request, 'blog/articles_par_categorie.html', {
        'categorie': categorie,
        'articles': articles
    })

# ✅ Création catégorie - Redirection custom si pas connecté
@never_cache
def ajouter_categorie(request):
    if not request.user.is_authenticated:
        messages.info(request, "Connectez-vous pour créer une catégorie.")
        return redirect('blog:login')
    
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catégorie créée avec succès !')
            return redirect('blog:liste_categories')
    else:
        form = CategorieForm()
    
    return render(request, 'blog/ajouter_categorie.html', {'form': form})