from django_filters import rest_framework as filters #un alias llamado filters
from apps.anuncio.models import Categoria

class CategoriaFilter(filters.FilterSet): #hereda de filterset
    nombre = filters.CharFilter(field_name='nombre', lookup_expr='icontains') #sobreescribo para que no sea por igualdad, que lo contenga por lo menos

    class Meta:
        model = Categoria
        fields = ['nombre', 'activa']


import django_filters
from apps.anuncio.models import Anuncio

class AnuncioFilter(django_filters.FilterSet):
    precio_min = django_filters.NumberFilter(field_name="precio_inicial", lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name="precio_inicial", lookup_expr='lte')

    fecha_inicio_min = django_filters.DateTimeFilter(field_name="fecha_inicio", lookup_expr='gte')
    fecha_inicio_max = django_filters.DateTimeFilter(field_name="fecha_inicio", lookup_expr='lte')

    categorias = django_filters.CharFilter(field_name='categorias__nombre', lookup_expr='iexact')

    class Meta:
        model = Anuncio
        fields = ['activo', 'publicado_por', 'categorias']

