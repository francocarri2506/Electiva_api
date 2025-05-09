
"""

from rest_framework import permissions

class EsDueñoOsoloLectura(permissions.BasePermission):

    #Permite solo al creador del anuncio editarlo o eliminarlo.
    #Otros usuarios solo pueden verlo (GET, HEAD, OPTIONS).


    def has_object_permission(self, request, view, obj):
        # Permitir siempre métodos de solo lectura (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Solo el creador del anuncio puede modificarlo o eliminarlo
        return obj.publicado_por == request.user


"""