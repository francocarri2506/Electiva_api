from rest_framework import serializers
from .models import Categoria, Anuncio


class CategoriaSerializer(serializers.ModelSerializer): #
    class Meta:
        model = Categoria
        fields = [
            'id',
            'nombre',
            'activa',
        ]

############ VALIDACIÓN A NIVEL DE CAMPO #########################


    def validate_nombre(self, value):
        # Verificar que el nombre no contenga la palabra "categoría"
        if "categoria" in value.lower():
            raise serializers.ValidationError("El nombre no puede contener la palabra 'categoría'.") #lanzo una instancia de error

        # validacion para no permitir categorías duplicadas

        if Categoria.objects.filter(nombre__iexact=value).exists():
            raise serializers.ValidationError("Ya existe una categoría con ese nombre.")

        # validar que no se creen categorias sin sentidos como de solo 1 o 2 letras

        if len(value.strip()) < 3:
            raise serializers.ValidationError("El nombre de la categoría debe tener al menos 3 caracteres.")

        return value


#########################  VALIDACIÓN A NIVEL DE OBJETO  #########################
#para validar mas de un valor para ello se una el metodo validate
    def validate(self, data): #un diccionario del objeto
        if 'principal' in data['nombre'].lower() and not data['activa']:
            raise serializers.ValidationError("No se puede desactivar la Categoria principal")
        return data



############ este era el serializador para el tp2 #########################
"""
class AnuncioSerializer(serializers.ModelSerializer):
    # categorias = serializers.StringRelatedField(many=True) #para mostrar el nombre de la categoria y no id
    class Meta:
        model = Anuncio
        fields = [
            'id',
            'titulo',
            'precio_inicial',
            #'fecha_publicacion',
            'categorias',
            'publicado_por',
            'oferta_ganadora'
        ]
        read_only_fields = [
            'publicado_por',
            'oferta_ganadora'
        ]

"""
""" 

class AnuncioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anuncio
        fields = '__all__'

class AnuncioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anuncio
        fields = [
            'id',
            'titulo',
            'descripcion',
            'precio_inicial',
            'imagen',
            'fecha_publicacion',
            'fecha_inicio',
            'fecha_fin',
            'activo',
            'categorias',
            'publicado_por',
            'oferta_ganadora',
        ]
        read_only_fields = ['fecha_publicacion', 'publicado_por', 'oferta_ganadora']

"""

"""
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)
"""

########## serializador para el tp3 ######################
"""
class AnuncioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anuncio
        fields = '__all__'
        read_only_fields = ['publicado_por', 'fecha_publicacion', 'oferta_ganadora']

"""
########## serializador para el tp3  mostrando el nombre de la categoria######################
"""
class AnuncioSerializer(serializers.ModelSerializer):
    categorias = serializers.SlugRelatedField(
        many=True,
        slug_field='nombre',
        queryset=Categoria.objects.all()
    )

    class Meta:
        model = Anuncio
        fields = '__all__'
        read_only_fields = ['publicado_por', 'fecha_publicacion', 'oferta_ganadora']

"""

from rest_framework import serializers
from datetime import datetime
from django.utils import timezone
from apps.anuncio.models import Anuncio, Categoria

class AnuncioSerializer(serializers.ModelSerializer):
    categorias = serializers.SlugRelatedField(
        many=True,
        slug_field='nombre',
        queryset=Categoria.objects.all()
    )
    publicado_por = serializers.StringRelatedField(read_only=True) #para mostrar el nombre de quien lo publico

    class Meta:
        model = Anuncio
        fields = '__all__'
        read_only_fields = ['publicado_por', 'fecha_publicacion', 'oferta_ganadora']

    def validate(self, data):
        fecha_inicio = data.get('fecha_inicio', None)
        fecha_fin = data.get('fecha_fin', None)
        precio = data.get('precio_inicial', None)
        categorias = data.get('categorias', [])

        # Validar que la fecha_inicio sea futura
        if fecha_inicio and fecha_inicio < timezone.now():
            raise serializers.ValidationError({
                'fecha_inicio': 'La fecha de inicio debe ser posterior a la fecha y hora actual.'
            })

        # Validar que la fecha_fin (si se ingresó) sea posterior a la fecha_inicio
        if fecha_inicio and fecha_fin and fecha_fin <= fecha_inicio:
            raise serializers.ValidationError({
                'fecha_fin': 'La fecha de fin debe ser posterior a la fecha de inicio.'
            })

        # Validar precio mayor a cero
        if precio is not None and precio <= 0:
            raise serializers.ValidationError({
                'precio_inicial': 'El precio inicial debe ser mayor a cero.'
            })

        # validar que una subasta no dure menos de 1 hora.
        #se puede cambiar para hacerla durar otro tiempo
        if fecha_inicio and fecha_fin:
            duracion = fecha_fin - fecha_inicio
            if duracion.total_seconds() < 3600:
                raise serializers.ValidationError("La subasta debe durar al menos 1 hora.")

        # Validar que las categorías estén activas
        for cat in categorias:
            if not cat.activa:
                raise serializers.ValidationError({
                    'categorias': f'La categoría "{cat.nombre}" está inactiva y no puede ser seleccionada.'
                })

        return data

#validacion a nivel de campo
""" 
    def validate_precio_inicial(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio inicial debe ser mayor que cero.")
       return value

"""


#--------------------------- tp5 --------------------------------------

# Desarrollar un endpoint para que un usuario diferente al creador de un anuncio, pueda realizar una oferta sobre el
# mismo, verificando que se encuentre activo al momento de la oferta.


from rest_framework import serializers
from .models import OfertaAnuncio

class OfertaAnuncioSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfertaAnuncio
        fields = ['id', 'precio_oferta', 'fecha_oferta', 'usuario', 'anuncio', 'es_ganador']
        read_only_fields = ['fecha_oferta', 'usuario', 'anuncio', 'es_ganador']