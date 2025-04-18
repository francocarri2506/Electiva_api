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