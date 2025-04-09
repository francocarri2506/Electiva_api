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