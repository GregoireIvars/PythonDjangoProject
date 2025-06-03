from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('ajouter/', views.ajouter_article, name='ajouter_article'),
    path('article/<int:article_id>/', views.detail_article, name='detail_article'),
    path('article/<int:article_id>/modifier/', views.modifier_article, name='modifier_article'),
    path('article/<int:article_id>/supprimer/', views.supprimer_article, name='supprimer_article'),
    path('profil/', views.profile, name='profile'),
    path('profil/modifier/', views.edit_profile, name='edit_profile'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_register, name='signup'),
    path('logout/', views.user_logout, name='logout'),
]