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
    
    # Catégories
    path('categories/', views.liste_categories, name='liste_categories'),
    path('categorie/<int:categorie_id>/', views.articles_par_categorie, name='articles_par_categorie'),
    path('ajouter-categorie/', views.ajouter_categorie, name='ajouter_categorie'),
    
    # ✅ Authentification dans le même namespace
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_register, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]