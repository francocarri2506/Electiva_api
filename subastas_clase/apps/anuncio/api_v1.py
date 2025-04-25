
from rest_framework import viewsets
from apps.anuncio.models import Anuncio, Categoria
from .serializers import AnuncioSerializer, CategoriaSerializer

class AnuncioViewSetV1(viewsets.ModelViewSet):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer

    def perform_create(self, serializer):
        serializer.save(publicado_por=self.request.user)


class CategoriaViewSetV1(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

