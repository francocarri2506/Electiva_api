"""

from rest_framework import viewsets, serializers
from apps.anuncio.models import Anuncio
from datetime import datetime
from django.utils import timezone

class AnuncioSerializerV2(serializers.ModelSerializer):
    dias_restantes = serializers.SerializerMethodField()

    class Meta:
        model = Anuncio
        fields = '__all__'

    def get_dias_restantes(self, obj):
        if obj.fecha_fin:
            delta = obj.fecha_fin - timezone.now()
            return max(delta.days, 0)
        return None

class AnuncioViewSetV2(viewsets.ModelViewSet):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializerV2

    def perform_create(self, serializer):
        serializer.save(publicado_por=self.request.user)

"""

from rest_framework import viewsets, serializers
from apps.anuncio.models import Anuncio, Categoria


class AnuncioSerializerV2(serializers.ModelSerializer):
    duracion_subasta = serializers.SerializerMethodField()

    class Meta:
        model = Anuncio
        fields = '__all__'

    def get_duracion_subasta(self, obj):
        if obj.fecha_inicio and obj.fecha_fin:
            return (obj.fecha_fin - obj.fecha_inicio).days
        return None

class AnuncioViewSetV2(viewsets.ModelViewSet):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializerV2

class CategoriaSerializerV2(serializers.ModelSerializer):
    nombre_mayus = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = '__all__'

    def get_nombre_mayus(self, obj):
        return obj.nombre.upper()

class CategoriaViewSetV2(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializerV2
