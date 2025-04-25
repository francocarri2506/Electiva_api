
"""
"""
from django.urls import path

from .api import CategoriaListaAPIView, CategoriaDetalleAPIView, AnuncioListaAPIView, AnuncioDetalleAPIView, \
    CategoriaListaGenericView, CategoriaDetalleGenericView, AnuncioListaGenericView, AnuncioDetalleGenericView

#from .views import AnuncioListaAPIView

app_name = 'anuncio'

urlpatterns = [
    path('api-view/categoria/', CategoriaListaAPIView.as_view()),
    path('api-view/categoria/<pk>/', CategoriaDetalleAPIView.as_view()),
    path('api-view/anuncio/', AnuncioListaAPIView.as_view()),
    path('api-view/anuncio/<int:pk>/', AnuncioDetalleAPIView.as_view()),
    path('generic-view/categoria/', CategoriaListaGenericView.as_view()),
    path('generic-view/categoria/<int:pk>/', CategoriaDetalleGenericView.as_view()),

    path('generic-view/anuncios/', AnuncioListaGenericView.as_view(), name='anuncio-lista'),
    path('generic-view/anuncios/<int:pk>/', AnuncioDetalleGenericView.as_view(), name='anuncio-detalle'),
]

"""

#------------------------versionado-------------------------------
# descomentar para probar el versionado y comentar lo de arriba
#hice 2 versioes muy basicas con la diferencia por ejemplo en categoria que 
#una muestra el nombre en mayusculas, el otro solo el id


from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importar viewsets
from apps.anuncio.api_v1 import AnuncioViewSetV1, CategoriaViewSetV1
from apps.anuncio.api_v2 import AnuncioViewSetV2, CategoriaViewSetV2


# Routers versión 1
router_v1 = DefaultRouter()
router_v1.register(r'anuncios', AnuncioViewSetV1)
router_v1.register(r'categorias', CategoriaViewSetV1)


# Routers versión 2
router_v2 = DefaultRouter()
router_v2.register(r'anuncios', AnuncioViewSetV2)
router_v2.register(r'categorias', CategoriaViewSetV2)


app_name = 'anuncio'

urlpatterns = [
    path('api/v1/', include(router_v1.urls)),
    path('api/v2/', include(router_v2.urls)),
]

"""