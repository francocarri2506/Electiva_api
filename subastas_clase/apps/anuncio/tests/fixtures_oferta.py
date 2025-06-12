import pytest
from django.utils import timezone
from datetime import timedelta
from apps.anuncio.models import Anuncio, Categoria

from django.contrib.auth import get_user_model

@pytest.fixture
def get_anuncio_para_oferta(django_user_model):
    creador = django_user_model.objects.create_user(
        username="creador",
        password="test1234",
        documento_identidad="11111111"
    )
    categoria, _ = Categoria.objects.get_or_create(nombre="Tecnología", defaults={"activa": True})

    fecha_inicio = timezone.now() + timedelta(hours=1)
    fecha_fin = fecha_inicio + timedelta(days=1)

    anuncio = Anuncio.objects.create(
        titulo="Notebook Lenovo i7",
        descripcion="Alta gama, poco uso.",
        precio_inicial=800.00,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        activo=True,
        publicado_por=creador
    )
    anuncio.categorias.add(categoria)

    return anuncio



User = get_user_model()

@pytest.fixture
def get_usuario_ofertante():
    return User.objects.create_user(
        username="ofertante",
        password="test1234",
        documento_identidad="22222222"
    )