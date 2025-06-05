# Blog Django avec IA

Un blog Django moderne avec génération d'articles par intelligence artificielle.

## 🚀 Fonctionnalités

- ✅ Création et gestion d'articles
- ✅ Système d'authentification complet
- ✅ Commentaires sur les articles
- ✅ Catégorisation des articles
- ✅ Support multilingue (français, anglais, espagnol)
- ✅ Panel d'administration avancé
- ✅ Génération d'articles par IA (OpenAI GPT)
- ✅ Génération d'images par IA (DALL-E)

## 🛠️ Installation et configuration

### Prérequis

- Python 3.8+
- Docker et Docker Compose
- Compte OpenAI avec clé API

### Configuration

1. **Cloner le projet**
   ```bash
   git clone <url-du-repo>
   cd AppPython
   ```

2. **Configurer les variables d'environnement**
   ```bash
   cp .env.example .env
   ```
   
   Puis éditez le fichier `.env` et remplissez vos propres valeurs :
   ```
   SECRET_KEY=your-secret-key-here
   OPENAI_API_KEY=your-openai-api-key-here
   DB_PASSWORD=your-db-password
   # ... autres variables
   ```

3. **Obtenir une clé API OpenAI**
   - Rendez-vous sur [OpenAI Platform](https://platform.openai.com/)
   - Créez un compte et générez une clé API
   - Ajoutez la clé dans votre fichier `.env`

4. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

5. **Lancer avec Docker**
   ```bash
   docker-compose up -d
   ```

6. **Effectuer les migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

7. **Créer un superutilisateur**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## 🔧 Utilisation

- Accédez à l'application : http://localhost:8000
- Panel d'admin : http://localhost:8000/admin
- Génération d'articles IA : http://localhost:8000/generer-article-ai

## 🔒 Sécurité

⚠️ **Important** : Ne jamais committer le fichier `.env` qui contient vos clés secrètes !

Le fichier `.gitignore` est configuré pour exclure automatiquement :
- `.env` (variables d'environnement)
- `media/` (fichiers uploadés)
- `__pycache__/` (cache Python)
- `*.log` (fichiers de logs)

## 📁 Structure du projet

```
AppPython/
├── .env.example          # Template des variables d'environnement
├── .gitignore           # Fichiers à exclure du versioning
├── docker-compose.yml   # Configuration Docker
├── requirements.txt     # Dépendances Python
└── backend/
    ├── manage.py
    ├── config/          # Configuration Django
    ├── blog/           # Application principale
    ├── locale/         # Fichiers de traduction
    └── media/          # Fichiers uploadés
```

## 🌍 Support multilingue

Le projet supporte 3 langues :
- Français (par défaut)
- Anglais
- Espagnol

Pour ajouter une nouvelle langue, consultez la documentation Django sur l'internationalisation.

## 🤖 IA et génération de contenu

Le projet utilise OpenAI pour :
- Générer le contenu des articles
- Créer des titres accrocheurs
- Générer des images avec DALL-E

Configuration requise dans `.env` :
```
OPENAI_API_KEY=your-openai-api-key
```

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
