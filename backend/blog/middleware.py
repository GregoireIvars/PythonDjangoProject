from django.utils.cache import add_never_cache_headers

class NoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # ✅ Headers anti-cache seulement pour les pages sensibles
        sensitive_paths = [
            '/ajouter/',
            '/modifier/', 
            '/profil/',
            '/login/',
            '/logout/',
            '/signup/',
            '/article/',  # Pages d'articles (pour commentaires)
        ]
        
        if any(path in request.path for path in sensitive_paths):
            add_never_cache_headers(response)
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response