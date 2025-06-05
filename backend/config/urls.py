from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# URLs non traduites (API, admin, etc.)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  # URLs pour changer de langue
]

# URLs traduites avec préfixe de langue
urlpatterns += i18n_patterns(
    path('', include('blog.urls')),  # Seulement blog.urls, pas auth_urls
    prefix_default_language=False,  # Ne pas préfixer la langue par défaut
)

# Servir les fichiers média en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)