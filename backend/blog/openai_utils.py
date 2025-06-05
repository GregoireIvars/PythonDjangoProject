import os
import requests
import tempfile
from urllib.request import urlretrieve
from django.core.files import File
from django.conf import settings

# Récupération de la clé API depuis les paramètres
OPENAI_API_KEY = settings.OPENAI_API_KEY

def generate_article_content(prompt, language='fr', max_tokens=2500):
    """
    Génère le contenu d'un article à partir d'un prompt en utilisant l'API OpenAI
    """
    # Adapter le prompt selon la langue
    lang_prompts = {
        'fr': f"Rédige un article complet et détaillé en français sur le sujet suivant: {prompt}. "
              f"L'article doit être bien structuré avec une introduction, des sections numérotées et une conclusion. "
              f"Utilise un ton professionnel et informatif.",
        'en': f"Write a complete and detailed article in English about: {prompt}. "
              f"The article must be well-structured with an introduction, numbered sections, and a conclusion. "
              f"Use a professional and informative tone.",
        'es': f"Escribe un artículo completo y detallado en español sobre: {prompt}. "
              f"El artículo debe estar bien estructurado con una introducción, secciones numeradas y una conclusión. "
              f"Utiliza un tono profesional e informativo."
    }
    
    # Utiliser le prompt par défaut en français si la langue n'est pas supportée
    final_prompt = lang_prompts.get(language, lang_prompts['fr'])
    
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-3.5-turbo',
                'messages': [{'role': 'user', 'content': final_prompt}],
                'max_tokens': max_tokens
            }
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Erreur: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Erreur lors de la génération du contenu: {str(e)}"

def generate_title(article_content, language='fr'):
    """
    Génère un titre accrocheur pour un article en utilisant son contenu
    """
    # Adapter le prompt selon la langue
    lang_prompts = {
        'fr': f"À partir de cet extrait d'article, génère un titre accrocheur et efficace en français (15 mots maximum): {article_content[:500]}...",
        'en': f"Based on this article excerpt, generate a catchy and effective title in English (maximum 15 words): {article_content[:500]}...",
        'es': f"A partir de este extracto de artículo, genera un título atractivo y eficaz en español (máximo 15 palabras): {article_content[:500]}..."
    }
    
    final_prompt = lang_prompts.get(language, lang_prompts['fr'])
    
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-3.5-turbo',
                'messages': [{'role': 'user', 'content': final_prompt}],
                'max_tokens': 50
            }
        )
        
        if response.status_code == 200:
            title = response.json()['choices'][0]['message']['content'].strip()
            # Nettoyer les guillemets éventuels
            title = title.strip('"').strip('"').strip("'").strip()
            return title
        else:
            return "Titre généré automatiquement"
            
    except Exception as e:
        return "Titre généré automatiquement"

def generate_image(prompt, language='fr'):
    """
    Génère une image pour l'article en utilisant DALL·E via l'API OpenAI
    """
    # Créer un prompt pour la description de l'image basée sur la langue
    lang_prompts = {
        'fr': f"Génère une description d'image pour illustrer ce sujet : {prompt}",
        'en': f"Generate an image description to illustrate this topic: {prompt}",
        'es': f"Genera una descripción de imagen para ilustrar este tema: {prompt}"
    }
    
    image_prompt = lang_prompts.get(language, lang_prompts['fr'])
    
    try:
        # 1. Génération de la description d'image
        image_desc_response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-3.5-turbo',
                'messages': [{'role': 'user', 'content': image_prompt}]
            }
        )
        
        if image_desc_response.status_code == 200:
            image_description = image_desc_response.json()['choices'][0]['message']['content']
            
            # 2. Génération de l'image avec DALL·E
            dalle_response = requests.post(
                'https://api.openai.com/v1/images/generations',
                headers={
                    'Authorization': f'Bearer {OPENAI_API_KEY}',
                    'Content-Type': 'application/json'
                },
                json={
                    'prompt': image_description,
                    'n': 1,
                    'size': '512x512'
                }
            )
            
            if dalle_response.status_code == 200:
                image_url = dalle_response.json()['data'][0]['url']
                
                # 3. Téléchargement de l'image générée
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                    urlretrieve(image_url, temp_file.name)
                    return temp_file.name
                    
        return None
    except Exception as e:
        print(f"Erreur lors de la génération d'image: {str(e)}")
        return None
