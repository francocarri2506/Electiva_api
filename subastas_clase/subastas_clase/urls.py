
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.anuncio.urls', namespace='anuncio')),

    #path('view-set/', include('subastas_clase.router')),
    path('api/', include('subastas_clase.router')), #para usar rutas como la profe


    #path('api/token-auth/', obtain_auth_token),  # Endpoint para obtener el token
    path('api/token-auth/', obtain_auth_token, name='api-token-auth'),
    path('api-auth/', include('rest_framework.urls')),# para loguearce



    # Ruta para generar el esquema OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Documentación Swagger interactiva
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Documentación Redoc (estática y ordenada)
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]
