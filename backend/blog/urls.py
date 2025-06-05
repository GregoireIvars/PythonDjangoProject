from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Pages principales
    path('', views.home, name='home'),
    path('article/<int:article_id>/', views.detail_article, name='detail_article'),
    
    # Articles
    path('ajouter/', views.ajouter_article, name='ajouter_article'),
    path('modifier/<int:article_id>/', views.modifier_article, name='modifier_article'),
    path('supprimer/<int:article_id>/', views.supprimer_article, name='supprimer_article'),
    path('generer-ai/', views.generer_article_ai, name='generer_article_ai'),  # Nouvelle URL pour IA
    
    # Catégories
    path('categories/', views.liste_categories, name='liste_categories'),
    path('categorie/<int:categorie_id>/', views.articles_par_categorie, name='articles_par_categorie'),
    path('ajouter-categorie/', views.ajouter_categorie, name='ajouter_categorie'),
    
    # Filtrage par langue
    path('articles/langue/<str:langue_code>/', views.articles_par_langue, name='articles_par_langue'),
    
    # Authentification
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_register, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    
    # ✅ Nouveaux URLs - Demande auteur
    path('demander-auteur/', views.demander_auteur, name='demander_auteur'),
    
    # ✅ Nouveaux URLs - Admin Panel
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/demandes/', views.admin_demandes, name='admin_demandes'),
    path('admin-panel/traiter-demande/<int:user_id>/', views.traiter_demande_auteur, name='traiter_demande_auteur'),
    path('admin-panel/utilisateurs/', views.admin_utilisateurs, name='admin_utilisateurs'),
    path('admin-panel/changer-role/<int:user_id>/', views.changer_role_user, name='changer_role_user'),
    path('admin-panel/articles/', views.admin_articles, name='admin_articles'),
    path('admin-panel/categories/', views.admin_categories, name='admin_categories'),
    path('admin-panel/supprimer-categorie/<int:categorie_id>/', views.supprimer_categorie, name='supprimer_categorie'),
]