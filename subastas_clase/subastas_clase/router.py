from rest_framework import routers
#from apps.anuncio.api import CategoriaViewSet, AnuncioViewSet

from apps.anuncio.api.api import CategoriaViewSet, AnuncioViewSet


# Inicializar el router
router = routers.DefaultRouter()

# Registrar el ViewSet
router.register(prefix='categoria', viewset=CategoriaViewSet)


router.register(prefix='anuncios', viewset=AnuncioViewSet)
#router.register(r'view-set/anuncios', AnuncioViewSet, basename='anuncio')

# Incluir las URLs generadas automáticamente
urlpatterns = router.urls

"""
# Ejemplo de Archivo router.py

from apps.anuncio.api import CategoriaViewSet, UserViewSet

# Registrar el ViewSet
router.register(prefix='users', viewset=UserViewSet)

"""