# 🚀 Blog Django avec Intelligence Artificielle

Un blog moderne et intelligent développé avec Django, intégrant les technologies d'OpenAI (GPT et DALL-E) pour la génération automatique de contenu et d'images. Ce projet propose un système de rôles avancé, un support multilingue complet et une interface d'administration intuitive.

## 📋 Table des Matières

- [🌟 Fonctionnalités](#-fonctionnalités)
- [🏗️ Architecture](#️-architecture)
- [📦 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [🚀 Démarrage](#-démarrage)
- [👤 Création du Compte Administrateur](#-création-du-compte-administrateur)
- [🎭 Système de Rôles](#-système-de-rôles)
- [🤖 Fonctionnalités IA](#-fonctionnalités-ia)
- [🌐 Support Multilingue](#-support-multilingue)
- [📱 Utilisation](#-utilisation)
- [🔒 Sécurité](#-sécurité)
- [🛠️ Développement](#️-développement)
- [🚀 Déploiement en Production](#-déploiement-en-production)

## 🌟 Fonctionnalités

### ✨ Fonctionnalités Principales
- **📝 Gestion d'articles** : Création, modification, suppression avec éditeur riche
- **🔐 Authentification complète** : Inscription, connexion, profils utilisateurs
- **💬 Système de commentaires** : Interaction communautaire sur les articles
- **🏷️ Catégorisation** : Organisation des articles par catégories
- **🌍 Support multilingue** : Français, Anglais, Espagnol
- **👥 Système de rôles** : Lecteur, Auteur, Administrateur
- **🎨 Interface moderne** : Design responsive avec Bootstrap 5

### 🤖 Intelligence Artificielle
- **📖 Génération d'articles** : Création automatique de contenu avec OpenAI GPT-3.5
- **🖼️ Génération d'images** : Illustrations automatiques avec DALL-E
- **🔤 Génération de titres** : Titres accrocheurs générés automatiquement
- **🌐 Support multilingue IA** : Génération de contenu dans les 3 langues

### 👑 Panel d'Administration
- **📊 Dashboard** : Statistiques complètes du blog
- **👤 Gestion des utilisateurs** : Modification des rôles et permissions
- **📋 Gestion des demandes** : Validation des demandes d'auteur
- **📰 Modération des articles** : Vue d'ensemble et gestion
- **🏷️ Gestion des catégories** : Création et organisation

## 🏗️ Architecture

```
AppPython/
├── backend/                 # Application Django principale
│   ├── blog/               # App principale du blog
│   │   ├── models.py       # Modèles de données
│   │   ├── views.py        # Logique métier
│   │   ├── forms.py        # Formulaires Django
│   │   ├── decorators.py   # Décorateurs de permissions
│   │   ├── openai_utils.py # Utilitaires IA
│   │   └── templates/      # Templates HTML
│   ├── config/             # Configuration Django
│   └── locale/             # Fichiers de traduction
├── static/                 # Fichiers statiques
├── media/                  # Fichiers uploadés
├── docker-compose.yml      # Configuration Docker
├── Dockerfile             # Image Docker
├── requirements.txt       # Dépendances Python
├── .env                   # Variables d'environnement (à créer)
├── .env.example          # Template des variables
└── .gitignore            # Fichiers à ignorer par Git
```

## 📦 Installation

### Prérequis
- Docker et Docker Compose
- Git
- Un compte OpenAI avec clé API (pour les fonctionnalités IA)

### 1. Cloner le projet
```bash
git clone <url-du-projet>
cd AppPython
```

### 2. Configuration des variables d'environnement
```bash
# Copier le template
cp .env.example .env

# Éditer le fichier .env avec vos valeurs
```

## ⚙️ Configuration

### Variables d'environnement (.env)
Créez un fichier `.env` à la racine du projet avec les valeurs suivantes :

```env
# Base de données PostgreSQL
DB_NAME=blog_database
DB_USER=blog_user
DB_PASSWORD=votre_mot_de_passe_db
DB_HOST=db
DB_PORT=5432

# Sécurité Django
SECRET_KEY=votre_cle_secrete_django_super_longue_et_aleatoire
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# OpenAI API (obligatoire pour les fonctionnalités IA)
OPENAI_API_KEY=votre_cle_api_openai

# Configuration Email (optionnel)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre.email@gmail.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe_app
```

### ⚠️ Important : Clé API OpenAI
1. Créez un compte sur [OpenAI Platform](https://platform.openai.com/)
2. Générez une clé API dans la section "API Keys"
3. Ajoutez-la dans votre fichier `.env`

## 🚀 Démarrage

### Lancement avec Docker
```bash
# Construction et démarrage des conteneurs
docker-compose up --build

# En mode détaché (arrière-plan)
docker-compose up -d --build
```

### Première exécution
```bash
# Appliquer les migrations de base de données
docker-compose exec web python backend/manage.py migrate

# Collecter les fichiers statiques
docker-compose exec web python backend/manage.py collectstatic --noinput

# Compiler les traductions
docker-compose exec web python backend/manage.py compilemessages
```

### Accès aux services
- **Blog** : http://localhost:8000
- **Base de données** : localhost:5432
- **PgAdmin** : http://localhost:5050 (admin@admin.com / admin)

## 👤 Création du Compte Administrateur

### Méthode 1 : Via Django Admin
```bash
# Créer un superutilisateur Django
docker-compose exec web python backend/manage.py createsuperuser

# Suivre les instructions pour créer le compte
```

### Méthode 2 : Via l'interface web
1. Inscrivez-vous normalement sur http://localhost:8000/signup/
2. Connectez-vous au conteneur web : `docker-compose exec web bash`
3. Ouvrez le shell Django : `python backend/manage.py shell`
4. Exécutez :
```python
from django.contrib.auth.models import User
from blog.models import UserProfile

# Récupérer votre utilisateur
user = User.objects.get(username='votre_nom_utilisateur')

# Modifier le rôle vers admin
profile = user.profile
profile.role = 'admin'
profile.save()

print(f"Utilisateur {user.username} est maintenant administrateur")
```

### Accès au panel d'administration
- **Django Admin** : http://localhost:8000/admin/
- **Panel Blog** : http://localhost:8000/admin-panel/

## 🎭 Système de Rôles

### 👤 Lecteur (Par défaut)
**Permissions :**
- ✅ Lecture des articles
- ✅ Ajout de commentaires
- ✅ Modification de son profil
- ✅ Demande de statut auteur

**Limitations :**
- ❌ Création d'articles
- ❌ Accès au panel d'administration

### ✍️ Auteur
**Permissions :**
- ✅ Toutes les permissions du lecteur
- ✅ Création d'articles
- ✅ Modification de ses propres articles
- ✅ Suppression de ses propres articles
- ✅ Génération d'articles par IA
- ✅ Génération d'images par IA

**Obtention du statut :**
1. Faire une demande via le profil
2. Attendre la validation par un administrateur

### 👑 Administrateur
**Permissions :**
- ✅ Toutes les permissions des rôles précédents
- ✅ Accès au panel d'administration complet
- ✅ Gestion des utilisateurs et rôles
- ✅ Validation des demandes d'auteur
- ✅ Modération de tous les articles
- ✅ Gestion des catégories
- ✅ Accès aux statistiques

## 🤖 Fonctionnalités IA

### 📝 Génération d'Articles
**Fonctionnement :**
1. Accédez à "Générer un article IA" (auteurs/admins uniquement)
2. Saisissez un prompt descriptif
3. Choisissez la langue (FR/EN/ES)
4. Sélectionnez une catégorie
5. Optionnel : génération d'image d'illustration

**Exemple de prompts :**
- "L'impact de l'intelligence artificielle sur l'éducation"
- "Guide complet du développement web moderne"
- "Les tendances technologiques de 2024"

### 🖼️ Génération d'Images
- Utilise DALL-E d'OpenAI
- Images 512x512 pixels
- Basée sur le contenu de l'article
- Génération automatique de descriptions
- Support multilingue pour les prompts

### ⚡ Processus de Génération
1. **Analyse du prompt** : L'IA comprend le sujet
2. **Génération du contenu** : Article structuré avec intro/sections/conclusion
3. **Création du titre** : Titre accrocheur automatique
4. **Génération d'image** : Illustration pertinente (optionnel)
5. **Finalisation** : Article prêt à être publié

## 🌐 Support Multilingue

### Langues Supportées
- 🇫🇷 **Français** (par défaut)
- 🇬🇧 **Anglais**
- 🇪🇸 **Espagnol**

### Fonctionnalités Multilingues
- Interface traduite automatiquement
- Articles rédigés dans la langue choisie
- Génération IA dans la langue sélectionnée
- Filtrage des articles par langue
- URL linguistiques : `/articles/langue/en/`

### Changement de Langue
- Menu déroulant dans la navigation
- Préférence sauvegardée en session
- Traduction instantanée de l'interface

## 📱 Utilisation

### 📖 Pour les Lecteurs
1. **Inscription** : Créez votre compte
2. **Navigation** : Explorez les articles par catégorie/langue
3. **Interaction** : Commentez et engagez-vous
4. **Profil** : Personnalisez vos informations

### ✍️ Pour les Auteurs
1. **Demande de statut** : Via votre profil
2. **Création d'articles** : Interface intuitive
3. **Gestion IA** : Utilisez les outils de génération
4. **Suivi** : Consultez vos statistiques

### 👑 Pour les Administrateurs
1. **Dashboard** : Vue d'ensemble des activités
2. **Gestion** : Utilisateurs, articles, catégories
3. **Modération** : Validation des demandes
4. **Analytics** : Statistiques détaillées

## 🔒 Sécurité

### 🛡️ Mesures Implémentées
- **Variables d'environnement** : Secrets protégés
- **Permissions basées sur les rôles** : Accès contrôlé
- **Protection CSRF** : Formulaires sécurisés
- **Validation des entrées** : Données nettoyées
- **Gestion des sessions** : Authentification sécurisée

### 🔐 Bonnes Pratiques
- Changez la `SECRET_KEY` en production
- Utilisez `DEBUG=False` en production
- Configurez `ALLOWED_HOSTS` correctement
- Rotez régulièrement les clés API
- Surveillez les logs d'accès

## 🛠️ Développement

### 🔄 Commandes Utiles
```bash
# Logs en temps réel
docker-compose logs -f web

# Shell Django
docker-compose exec web python backend/manage.py shell

# Migrations
docker-compose exec web python backend/manage.py makemigrations
docker-compose exec web python backend/manage.py migrate

# Tests
docker-compose exec web python backend/manage.py test

# Collecte des fichiers statiques
docker-compose exec web python backend/manage.py collectstatic

# Compilation des traductions
docker-compose exec web python backend/manage.py compilemessages
```

### 🐛 Dépannage

#### Problèmes Courants et Solutions

**🔴 Erreur de connexion à la base de données**
```bash
# Vérifier le statut des conteneurs
docker-compose ps

# Redémarrer les services
docker-compose down && docker-compose up --build

# Vérifier les logs de la base de données
docker-compose logs db
```

**🔴 Clé API OpenAI invalide**
- Vérifiez que votre clé API est correcte dans le fichier `.env`
- Assurez-vous d'avoir du crédit sur votre compte OpenAI
- Testez votre clé API avec curl :
```bash
curl -H "Authorization: Bearer VOTRE_CLE_API" https://api.openai.com/v1/models
```

**🔴 Erreur de permissions Docker**
```bash
# Linux/Mac : Ajouter votre utilisateur au groupe docker
sudo usermod -aG docker $USER

# Windows : Vérifier que Docker Desktop fonctionne
```

**🔴 Port déjà utilisé (8000)**
```bash
# Trouver le processus utilisant le port
netstat -tulpn | grep :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Changer le port dans docker-compose.yml
ports:
  - "8001:8000"  # Utiliser le port 8001 à la place
```

**🔴 Problèmes de traductions**
```bash
# Regénérer les fichiers de traduction
docker-compose exec web python backend/manage.py makemessages -l fr
docker-compose exec web python backend/manage.py makemessages -l en
docker-compose exec web python backend/manage.py makemessages -l es
docker-compose exec web python backend/manage.py compilemessages
```

**🔴 Images non affichées**
```bash
# Vérifier la configuration des médias
docker-compose exec web python backend/manage.py collectstatic --noinput

# Vérifier les permissions des dossiers média
ls -la media/
```

**🔴 Erreurs lors de la génération IA**
- Vérifiez votre quota OpenAI
- Assurez-vous que les modèles `gpt-3.5-turbo` et `dall-e-2` sont disponibles
- Consultez les logs : `docker-compose logs web`

#### 📊 Monitoring et Logs

**Surveillance en temps réel :**
```bash
# Logs de l'application
docker-compose logs -f web

# Logs de la base de données
docker-compose logs -f db

# Statistiques des conteneurs
docker stats

# Espace disque des volumes
docker system df
```

**Debug Mode :**
```bash
# Activer le mode debug (à ne pas faire en production)
# Dans le fichier .env
DEBUG=True

# Redémarrer l'application
docker-compose restart web
```

### 📊 Base de Données
- **PostgreSQL 15** avec persistance
- **Migrations automatiques** au démarrage
- **PgAdmin** pour l'administration
- **Sauvegarde** : Volume Docker persistant

### 🎨 Frontend
- **Bootstrap 5** pour le design
- **FontAwesome** pour les icônes
- **Templates Django** avec héritage
- **CSS personnalisé** responsive

### 🔧 Architecture Technique

#### Structure des Modèles
```python
# Modèles principaux
- User (Django) : Utilisateurs
- UserProfile : Profils étendus avec rôles
- Article : Articles du blog
- Categorie : Catégories d'articles
- Commentaire : Commentaires sur articles
```

#### API OpenAI
```python
# Fonctions principales dans openai_utils.py
- generate_article_content() : Génération d'articles
- generate_title() : Génération de titres
- generate_image() : Génération d'images DALL-E
```

#### Système de Permissions
```python
# Décorateurs personnalisés
- @require_author : Accès auteurs/admins
- @require_admin : Accès admins uniquement
- @require_article_owner_or_admin : Propriétaire ou admin
```

### 🌐 URLs et Endpoints

#### Endpoints Publics
```
GET  /                          # Page d'accueil
GET  /articles/<id>/            # Détail d'un article
POST /articles/<id>/            # Ajouter un commentaire
GET  /categories/               # Liste des catégories
GET  /articles/categorie/<id>/  # Articles par catégorie
GET  /articles/langue/<code>/   # Articles par langue
```

#### Authentification
```
GET  /login/                    # Page de connexion
POST /login/                    # Traitement connexion
GET  /signup/                   # Page d'inscription
POST /signup/                   # Traitement inscription
GET  /logout/                   # Déconnexion
GET  /profile/                  # Profil utilisateur
GET  /edit-profile/             # Modification profil
POST /demander-auteur/          # Demande statut auteur
```

#### Auteurs/Admins
```
GET  /ajouter-article/          # Formulaire création article
POST /ajouter-article/          # Traitement création
GET  /modifier-article/<id>/    # Modification article
POST /modifier-article/<id>/    # Traitement modification
POST /supprimer-article/<id>/   # Suppression article
GET  /generer-article-ai/       # Interface IA
POST /generer-article-ai/       # Génération IA
```

#### Administration
```
GET  /admin-panel/              # Dashboard admin
GET  /admin-panel/utilisateurs/ # Gestion utilisateurs
GET  /admin-panel/demandes/     # Demandes d'auteur
GET  /admin-panel/articles/     # Gestion articles
GET  /admin-panel/categories/   # Gestion catégories
POST /admin-panel/changer-role/<id>/ # Changer rôle
```

### 📱 Interface Mobile

Le blog est entièrement responsive et optimisé pour :
- **📱 Smartphones** : Menu hamburger, cartes adaptées
- **💻 Tablettes** : Layout en colonnes, navigation tactile
- **🖥️ Desktop** : Interface complète, sidebar dynamique

### ⚡ Performance

#### Optimisations Implémentées
- **Cache Django** : Templates et requêtes mis en cache
- **Images optimisées** : Compression automatique des uploads
- **CSS/JS minifiés** : Fichiers statiques optimisés
- **Lazy Loading** : Chargement différé des images
- **CDN Ready** : Structure prête pour un CDN

#### Métriques Recommandées
```bash
# Taille de la base de données
docker-compose exec db psql -U postgres -d postgresSQL_db -c "SELECT pg_size_pretty(pg_database_size('postgresSQL_db'));"

# Nombre d'utilisateurs actifs
docker-compose exec web python backend/manage.py shell -c "from django.contrib.auth.models import User; print(f'Users: {User.objects.count()}')"

# Espace disque utilisé
du -sh media/
```

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche feature
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📞 Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation Django
- Vérifiez les logs : `docker-compose logs web`

---

**Développé avec ❤️ par votre équipe de développement**

## 🚀 Déploiement en Production

### 🔒 Configuration Production

#### Variables d'environnement (.env.production)
```env
# IMPORTANT : Valeurs pour la production
DEBUG=False
SECRET_KEY=votre_cle_secrete_production_tres_longue_et_aleatoire
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com

# Base de données production
DB_NAME=blog_production
DB_USER=blog_user_prod
DB_PASSWORD=mot_de_passe_super_securise
DB_HOST=db-production.example.com
DB_PORT=5432

# OpenAI API
OPENAI_API_KEY=votre_cle_openai_production

# Email SMTP
EMAIL_HOST=smtp.votre-domaine.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@votre-domaine.com
EMAIL_HOST_PASSWORD=mot_de_passe_email
```

#### Docker Compose Production
```yaml
# docker-compose.prod.yml
version: "3.9"

services:
  web:
    build: .
    command: bash -c "cd backend && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"
    volumes:
      - static_volume:/app/backend/staticfiles
      - media_volume:/app/backend/media
    environment:
      - DEBUG=False
    depends_on:
      - db
      - redis

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web

  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data

volumes:
  static_volume:
  media_volume:
  redis_data:
```

### 🌐 Serveur Web (Nginx)

#### Configuration Nginx
```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream django {
        server web:8000;
    }

    server {
        listen 80;
        server_name votre-domaine.com www.votre-domaine.com;

        location / {
            return 301 https://$server_name$request_uri;
        }
    }

    server {
        listen 443 ssl;
        server_name votre-domaine.com www.votre-domaine.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /static/ {
            alias /app/staticfiles/;
        }

        location /media/ {
            alias /app/media/;
        }
    }
}
```

### 🛡️ Sécurité Production

#### Checklist Sécurité
- ✅ `DEBUG=False` obligatoire
- ✅ Clé secrète unique et complexe
- ✅ HTTPS avec certificat SSL/TLS
- ✅ Base de données séparée et sécurisée
- ✅ Logs de sécurité activés
- ✅ Sauvegardes automatiques
- ✅ Pare-feu configuré
- ✅ Mises à jour régulières

#### Commandes de Déploiement
```bash
# Construction pour la production
docker-compose -f docker-compose.prod.yml build --no-cache

# Démarrage en production
docker-compose -f docker-compose.prod.yml up -d

# Migrations en production
docker-compose -f docker-compose.prod.yml exec web python backend/manage.py migrate

# Collecte des fichiers statiques
docker-compose -f docker-compose.prod.yml exec web python backend/manage.py collectstatic --noinput

# Création du superutilisateur
docker-compose -f docker-compose.prod.yml exec web python backend/manage.py createsuperuser
```

### 📊 Monitoring Production

#### Logs et Surveillance
```bash
# Logs de l'application
docker-compose -f docker-compose.prod.yml logs -f web

# Monitoring des ressources
docker stats

# Santé des conteneurs
docker-compose -f docker-compose.prod.yml ps
```

#### Métriques Importantes
- **Temps de réponse** : < 500ms
- **Uptime** : > 99.9%
- **Usage CPU** : < 80%
- **Usage RAM** : < 85%
- **Espace disque** : < 90%

### 🔄 Sauvegarde et Récupération

#### Sauvegarde Base de Données
```bash
# Sauvegarde quotidienne
docker-compose exec db pg_dump -U postgres postgresSQL_db > backup_$(date +%Y%m%d).sql

# Script de sauvegarde automatique
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec db pg_dump -U postgres postgresSQL_db | gzip > $BACKUP_DIR/blog_backup_$DATE.sql.gz
```

#### Sauvegarde Fichiers Media
```bash
# Synchronisation des médias
rsync -av media/ /backup/media/

# Sauvegarde sur cloud (exemple AWS S3)
aws s3 sync media/ s3://mon-bucket/media/
```

---
