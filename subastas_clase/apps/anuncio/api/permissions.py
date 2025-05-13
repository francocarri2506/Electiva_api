

from rest_framework import permissions

class EsDueñoDelAnuncio(permissions.BasePermission):

    """
    Permite acceso solo al usuario creador del anuncio.
    """

    def has_object_permission(self, request, view, obj):
        return obj.publicado_por == request.user



from rest_framework.permissions import BasePermission

class EsCreadorDelAnuncio(BasePermission):
    message = 'Solo el creador del anuncio puede modificar o eliminarlo.'

    # Permite solo al creador del anuncio editarlo o eliminarlo.
    # Otros usuarios solo pueden verlo (GET, HEAD, OPTIONS).

    def has_object_permission(self, request, view, obj):
        # Solo el creador puede modificar/eliminar
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.publicado_por == request.user
        return True