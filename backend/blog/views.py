from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.utils.translation import get_language
from django.core.files import File
import os
from .models import Article, Commentaire, Categorie, UserProfile
from .forms import ArticleForm, UserRegistrationForm, UserProfileForm, DemandeAuteurForm, CategorieForm, SimpleCommentForm
from .forms_ai import AIArticleGenerationForm
from .decorators import require_author, require_admin, require_article_owner_or_admin
from .openai_utils import generate_article_content, generate_title, generate_image
from django.views.decorators.csrf import csrf_protect

# ✅ HOME - Accessible à tous avec filtrage par langue
@never_cache
def home(request):
    articles = Article.objects.all().order_by('-date_publication')
    
    # Filtrage par langue si spécifié
    language_filter = request.GET.get('lang')
    if language_filter:
        articles = articles.filter(langue=language_filter)
    
    total_articles = articles.count()
    total_users = User.objects.count()
    
    context = {
        'articles': articles,
        'total_articles': total_articles,
        'total_users': total_users,
        'is_public_view': not request.user.is_authenticated,
        'current_language_filter': language_filter,
        'available_languages': Article.LANGUE_CHOICES,
    }
    return render(request, 'blog/home.html', context)

# ✅ DETAIL ARTICLE - Accessible à tous, redirection seulement pour commentaires
@never_cache
def detail_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    commentaires = article.commentaires.all().order_by('-date_publication')
    
    # ✅ Commentaires avec gestion CSRF correcte
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.info(request, "Connectez-vous pour pouvoir commenter cet article.")
            return redirect('blog:login')
        
        # ✅ Utiliser le formulaire Django pour les commentaires
        form = SimpleCommentForm(request.POST)
        if form.is_valid():
            contenu = form.cleaned_data['contenu']
            Commentaire.objects.create(
                article=article,
                auteur=request.user,
                contenu=contenu
            )
            messages.success(request, "Commentaire ajouté avec succès.")
            return redirect('blog:detail_article', article_id=article.id)
        else:
            messages.error(request, "Erreur dans le commentaire.")
    else:
        form = SimpleCommentForm()
    
    # ✅ Vérification permissions pour modification (avec rôles)
    user_role = 'lecteur'
    if request.user.is_authenticated:
        try:
            user_role = request.user.profile.role
        except:
            user_role = 'lecteur'
    
    peut_modifier = request.user.is_authenticated and (
        article.auteur == request.user or user_role == 'admin'
    )
    
    context = {
        'article': article,
        'commentaires': commentaires,
        'peut_modifier': peut_modifier,
        'peut_commenter': request.user.is_authenticated,
        'comment_form': form,  # ✅ Passer le formulaire au template
    }
    return render(request, 'blog/detail_article.html', context)

# ✅ CREATION ARTICLE - Auteurs et admins uniquement
@require_author
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

# ✅ MODIFICATION ARTICLE - Propriétaire ou admin
@require_article_owner_or_admin
@never_cache
def modifier_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article modifié avec succès !')
            return redirect('blog:detail_article', article_id=article.id)
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'blog/modifier_article.html', {'form': form, 'article': article})

# ✅ SUPPRESSION ARTICLE - Propriétaire ou admin
@require_article_owner_or_admin
@never_cache
def supprimer_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        titre = article.titre
        article.delete()
        messages.success(request, f'Article "{titre}" supprimé avec succès.')
        return redirect('blog:home')
    
    return render(request, 'blog/confirmer_suppression.html', {'article': article})

# ✅ AUTHENTIFICATION COMPLÈTE
@never_cache
@csrf_protect
def user_login(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {user.first_name or user.username} !')
                
                # Redirection après connexion
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('blog:home')
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
        else:
            messages.error(request, 'Veuillez remplir tous les champs.')
    
    return render(request, 'auth/login.html')

# ✅ INSCRIPTION COMPLÈTE
@never_cache
def user_register(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Message différent selon demande auteur
            if form.cleaned_data.get('demander_auteur'):
                messages.success(request, 'Compte créé avec succès ! Votre demande d\'auteur sera examinée par un administrateur.')
            else:
                messages.success(request, 'Compte créé avec succès ! Vous pouvez maintenant vous connecter.')
            return redirect('blog:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/signup.html', {'form': form})

@login_required
@never_cache
def user_logout(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('blog:home')

# ✅ PROFIL - Mise à jour avec informations demande auteur
@never_cache
def profile(request):
    if not request.user.is_authenticated:
        messages.info(request, "Connectez-vous pour accéder à votre profil.")
        return redirect('blog:login')
    
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # ✅ Articles de l'utilisateur si auteur/admin
    mes_articles = []
    if profile.peut_creer_articles():
        mes_articles = Article.objects.filter(auteur=request.user).order_by('-date_publication')
    
    context = {
        'profile': profile,
        'mes_articles': mes_articles,
    }
    return render(request, 'auth/profile.html', context)

# ✅ EDIT PROFILE COMPLET
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

# ✅ NOUVELLE VUE - Demande auteur depuis profil
@never_cache
def demander_auteur(request):
    if not request.user.is_authenticated:
        messages.info(request, "Connectez-vous pour faire une demande d'auteur.")
        return redirect('blog:login')
    
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if not profile.peut_demander_auteur():
        messages.error(request, "Vous ne pouvez pas faire de demande d'auteur actuellement.")
        return redirect('blog:profile')
    
    if request.method == 'POST':
        form = DemandeAuteurForm(request.POST)
        if form.is_valid():
            profile.demande_auteur_statut = 'en_attente'
            profile.demande_auteur_date = timezone.now()
            profile.demande_auteur_message = form.cleaned_data['message']
            profile.admin_reponse = ''
            profile.admin_reponse_date = None
            profile.save()
            
            messages.success(request, 'Votre demande d\'auteur a été envoyée ! Un administrateur l\'examinera bientôt.')
            return redirect('blog:profile')
    else:
        form = DemandeAuteurForm()
    
    return render(request, 'auth/demande_auteur.html', {'form': form})

# ✅ Catégories - Accessibles à tous
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

@never_cache
def articles_par_langue(request, langue_code):
    """Vue pour afficher les articles filtrés par langue"""
    # Vérifier que le code de langue est valide
    langues_valides = dict(Article.LANGUE_CHOICES)
    if langue_code not in langues_valides:
        messages.error(request, f'Code de langue invalide: {langue_code}')
        return redirect('blog:home')
    
    articles = Article.objects.filter(langue=langue_code).order_by('-date_publication')
    langue_nom = langues_valides[langue_code]
    
    context = {
        'articles': articles,
        'langue_code': langue_code,
        'langue_nom': langue_nom,
        'available_languages': Article.LANGUE_CHOICES,
    }
    return render(request, 'blog/articles_par_langue.html', context)

# ✅ CREATION CATEGORIE - Admin uniquement
@require_admin
@never_cache
def ajouter_categorie(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catégorie créée avec succès !')
            return redirect('blog:liste_categories')
    else:
        form = CategorieForm()
    
    return render(request, 'blog/ajouter_categorie.html', {'form': form})

# ========================================
# ✅ NOUVELLES VUES ADMIN PANEL
# ========================================

@require_admin
@never_cache
def admin_panel(request):
    """Dashboard administrateur principal"""
    # Statistiques générales
    stats = {
        'total_users': User.objects.count(),
        'total_articles': Article.objects.count(),
        'total_commentaires': Commentaire.objects.count(),
        'total_categories': Categorie.objects.count(),
        'demandes_en_attente': UserProfile.objects.filter(demande_auteur_statut='en_attente').count(),
        'auteurs_actifs': UserProfile.objects.filter(role='auteur').count(),
    }
    
    # Demandes en attente
    demandes_en_attente = UserProfile.objects.filter(
        demande_auteur_statut='en_attente'
    ).select_related('user').order_by('-demande_auteur_date')[:5]
    
    # Articles récents
    articles_recents = Article.objects.select_related('auteur').order_by('-date_publication')[:5]
    
    # Commentaires récents
    commentaires_recents = Commentaire.objects.select_related('auteur', 'article').order_by('-date_publication')[:5]
    
    context = {
        'stats': stats,
        'demandes_en_attente': demandes_en_attente,
        'articles_recents': articles_recents,
        'commentaires_recents': commentaires_recents,
    }
    return render(request, 'admin/panel.html', context)

@require_admin
@never_cache
def admin_demandes(request):
    """Gestion des demandes d'auteur"""
    demandes_en_attente = UserProfile.objects.filter(
        demande_auteur_statut='en_attente'
    ).select_related('user').order_by('-demande_auteur_date')
    
    demandes_traitees = UserProfile.objects.filter(
        demande_auteur_statut__in=['acceptee', 'refusee']
    ).select_related('user').order_by('-admin_reponse_date')[:10]
    
    context = {
        'demandes_en_attente': demandes_en_attente,
        'demandes_traitees': demandes_traitees,
    }
    return render(request, 'admin/demandes.html', context)

@require_admin
@never_cache
def traiter_demande_auteur(request, user_id):
    """Traiter une demande d'auteur (accepter/refuser)"""
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user_id=user_id)
        action = request.POST.get('action')
        reponse = request.POST.get('reponse', '')
        
        if action == 'accepter':
            profile.role = 'auteur'
            profile.demande_auteur_statut = 'acceptee'
            profile.admin_reponse = reponse
            profile.admin_reponse_date = timezone.now()
            profile.save()
            
            messages.success(request, f'Demande de {profile.user.username} acceptée ! Il est maintenant auteur.')
            
        elif action == 'refuser':
            profile.demande_auteur_statut = 'refusee'
            profile.admin_reponse = reponse
            profile.admin_reponse_date = timezone.now()
            profile.save()
            
            messages.info(request, f'Demande de {profile.user.username} refusée.')
    
    return redirect('blog:admin_demandes')

@require_admin
@never_cache
def admin_utilisateurs(request):
    """Gestion des utilisateurs"""
    users = User.objects.select_related('profile').order_by('-date_joined')
    
    # Filtres
    role_filter = request.GET.get('role')
    if role_filter:
        users = users.filter(profile__role=role_filter)
    
    context = {
        'users': users,
        'role_filter': role_filter,
        'roles': UserProfile.ROLE_CHOICES,
    }
    return render(request, 'admin/utilisateurs.html', context)

@require_admin
@never_cache
def changer_role_user(request, user_id):
    """Changer le rôle d'un utilisateur"""
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user_id=user_id)
        nouveau_role = request.POST.get('role')
        
        if nouveau_role in dict(UserProfile.ROLE_CHOICES):
            ancien_role = profile.get_role_display()
            profile.role = nouveau_role
            profile.save()
            
            messages.success(request, f'Rôle de {profile.user.username} changé de {ancien_role} à {profile.get_role_display()}.')
        else:
            messages.error(request, 'Rôle invalide.')
    
    return redirect('blog:admin_utilisateurs')

@require_admin
@never_cache
def admin_articles(request):
    """Gestion des articles par admin"""
    articles = Article.objects.select_related('auteur', 'categorie').order_by('-date_publication')
    
    # Filtres
    auteur_filter = request.GET.get('auteur')
    if auteur_filter:
        articles = articles.filter(auteur__username__icontains=auteur_filter)
    
    context = {
        'articles': articles,
        'auteur_filter': auteur_filter,
    }
    return render(request, 'admin/articles.html', context)

@require_admin
@never_cache
def admin_categories(request):
    """Gestion des catégories"""
    categories = Categorie.objects.annotate(
        nb_articles=models.Count('articles')
    ).order_by('nom')
    
    context = {
        'categories': categories,
    }
    return render(request, 'admin/categories.html', context)

@require_admin
@never_cache
def supprimer_categorie(request, categorie_id):
    """Supprimer une catégorie"""
    if request.method == 'POST':
        categorie = get_object_or_404(Categorie, id=categorie_id)
        nom = categorie.nom
        categorie.delete()
        messages.success(request, f'Catégorie "{nom}" supprimée avec succès.')
    
    return redirect('blog:admin_categories')

# ✅ GÉNÉRATION D'ARTICLE PAR IA - Auteurs et admins uniquement
@require_author
@never_cache
def generer_article_ai(request):
    if request.method == 'POST':
        form = AIArticleGenerationForm(request.POST)
        if form.is_valid():
            # Récupération des données du formulaire
            prompt = form.cleaned_data['prompt']
            langue = form.cleaned_data['langue']
            categorie = form.cleaned_data['categorie']
            titre_suggere = form.cleaned_data['titre']
            generer_image = form.cleaned_data['generer_image']
            
            try:
                # Initialiser la session avec les étapes de progression
                request.session['ai_generation'] = {
                    'total_steps': 3 + (1 if generer_image else 0),
                    'current_step': 1,
                    'step_name': 'contenu'
                }
                
                # 1. Génération du contenu de l'article
                messages.info(request, 'Génération du contenu de l\'article en cours...')
                contenu = generate_article_content(prompt, language=langue)
                
                if not contenu or "Erreur" in contenu:
                    messages.error(request, f'Échec de la génération du contenu: {contenu}')
                    # Ajouter contexte d'erreur pour le JS
                    return render(request, 'blog/generer_article_ai.html', {
                        'form': form,
                        'error_occurred': True
                    })
                
                # Mise à jour de la progression
                request.session['ai_generation']['current_step'] = 2
                request.session['ai_generation']['step_name'] = 'titre'
                request.session.modified = True
                
                # 2. Génération ou utilisation du titre fourni
                if not titre_suggere:
                    messages.info(request, 'Génération du titre en cours...')
                    titre = generate_title(contenu, language=langue)
                else:
                    titre = titre_suggere
                
                # Mise à jour de la progression
                request.session['ai_generation']['current_step'] = 3
                request.session['ai_generation']['step_name'] = 'article'
                request.session.modified = True
                
                # 3. Création de l'article
                article = Article(
                    titre=titre,
                    contenu=contenu,
                    auteur=request.user,
                    categorie=categorie,
                    langue=langue
                )
                
                # 4. Génération d'image si demandé
                if generer_image:
                    # Mise à jour de la progression
                    request.session['ai_generation']['current_step'] = 4
                    request.session['ai_generation']['step_name'] = 'image'
                    request.session.modified = True
                    
                    messages.info(request, 'Génération de l\'image en cours...')
                    image_path = generate_image(prompt, language=langue)
                    
                    if image_path:
                        # Ouverture et sauvegarde de l'image
                        with open(image_path, 'rb') as img_file:
                            article.images.save(
                                f"{titre[:30].replace(' ', '_')}.png", 
                                File(img_file), 
                                save=False
                            )
                        # Supprimer le fichier temporaire
                        os.remove(image_path)
                
                # 5. Sauvegarde de l'article
                article.save()
                
                # Nettoyage de la session
                if 'ai_generation' in request.session:
                    del request.session['ai_generation']
                
                messages.success(request, 'Article généré et publié avec succès !')
                return redirect('blog:detail_article', article_id=article.id)
                
            except Exception as e:
                # Nettoyage de la session en cas d'erreur
                if 'ai_generation' in request.session:
                    del request.session['ai_generation']
                
                messages.error(request, f'Une erreur est survenue: {str(e)}')
                # Ajouter contexte d'erreur pour le JS
                return render(request, 'blog/generer_article_ai.html', {
                    'form': form,
                    'error_occurred': True
                })
    else:
        # Nettoyage de la session si on accède au formulaire
        if 'ai_generation' in request.session:
            del request.session['ai_generation']
            
        form = AIArticleGenerationForm()
    
    return render(request, 'blog/generer_article_ai.html', {'form': form})