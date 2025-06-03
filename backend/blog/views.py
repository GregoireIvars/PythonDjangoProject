from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Article, Commentaire, Categorie
from .forms import ArticleForm, CommentaireForm, CategorieForm

def home(request):
    articles = Article.objects.all()
    categories_count = Categorie.objects.count()
    return render(request, 'blog/home.html', {
        'articles': articles,
        'categories_count': categories_count,
    })
def ajouter_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)  # Assurez-vous de gérer les fichiers
        if form.is_valid():
            form.save()
            messages.success(request, "L'article a été ajouté avec succès.")
            return redirect('home')  # ou autre url
    else:
        form = ArticleForm()
    return render(request, 'blog/ajouter_article.html', {'form': form})
def detail_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    commentaires = Commentaire.objects.filter(article=article).order_by('-date_publication')

    if request.method == 'POST':
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.article = article
            commentaire.save()
            messages.success(request, "Commentaire ajouté avec succès.")
            return redirect('detail_article', pk=article.pk)
    else:
        form = CommentaireForm()

    return render(request, 'blog/detail_article.html', {
        'article': article,
        'form': form,
        'commentaires': commentaires,
    })
    
def supprimer_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    messages.success(request, "L'article a été supprimé avec succès.")
    return redirect('home')

def modifier_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "L'article a été modifié avec succès.")
            return redirect('home')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/modifier_article.html', {'form': form, 'article': article})
def ajouter_categorie(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "La catégorie a été créée avec succès.")
            return redirect('liste_categories')
    else:
        form = CategorieForm()
    return render(request, 'blog/ajouter_categorie.html', {'form': form})
def liste_categories(request):
    categories = Categorie.objects.all()
    return render(request, 'blog/liste_categories.html', {'categories': categories})
def articles_par_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    articles = Article.objects.filter(categorie=categorie)
    return render(request, 'blog/articles_par_categorie.html', {
        'categorie': categorie,
        'articles': articles
    })