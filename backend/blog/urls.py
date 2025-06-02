from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ajouter/', views.ajouter_article, name='ajouter_article'),
    path('modifier/<int:pk>/', views.modifier_article, name='modifier_article'),
    path('article/<int:pk>/', views.detail_article, name='detail_article'),
    path('article/<int:pk>/supprimer/', views.supprimer_article, name='supprimer_article'),
    path('categories/', views.liste_categories, name='liste_categories'),
    path('categories/ajouter/', views.ajouter_categorie, name='ajouter_categorie'),
    path('categories/<int:categorie_id>/', views.articles_par_categorie, name='articles_par_categorie'),
]