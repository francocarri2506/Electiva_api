# apps/anuncio/tests/fixtures_anuncio.py
import pytest
from django.contrib.auth.models import User
from apps.anuncio.models import Categoria, Anuncio
from django.utils import timezone
from datetime import timedelta

from apps.usuario.models import Usuario


@pytest.fixture
def categoria_activa():
    categoria, _ = Categoria.objects.get_or_create(
        nombre='Tecnología',
        defaults={"activa": True}
    )
    return categoria


@pytest.fixture
def get_anuncio_modificable(get_user_generico, categoria_activa):
    fecha_inicio = timezone.now() + timedelta(hours=2)
    fecha_fin = fecha_inicio + timedelta(hours=2)

    anuncio = Anuncio.objects.create(
        titulo="Xbox Series X",
        descripcion="Consola potente",
        precio_inicial=450.00,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        activo=True,
        publicado_por=get_user_generico
    )
    anuncio.categorias.add(categoria_activa)
    return anuncio


@pytest.fixture
def usuario_dueño(db):
    return Usuario.objects.create_user(
        username="dueño",
        password="test1234",
        documento_identidad="12345678"
    )

@pytest.fixture
def usuario_intruso(db):
    return Usuario.objects.create_user(
        username="intruso",
        password="test1234",
        documento_identidad="87654321"
    )


@pytest.fixture
def anuncio_de_otro_usuario(usuario_dueño, categoria_activa):
    fecha_inicio = timezone.now() + timedelta(hours=2)
    fecha_fin = fecha_inicio + timedelta(hours=2)

    anuncio = Anuncio.objects.create(
        titulo="Samsung A32",
        descripcion="Anuncio de prueba",
        precio_inicial=1500.00,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        activo=True,
        publicado_por=usuario_dueño
    )
    anuncio.categorias.add(categoria_activa)
    return anuncio



@pytest.fixture
def get_anuncios(get_user_generico):
    usuario = get_user_generico
    ahora = timezone.now()
    fecha_inicio = ahora + timedelta(hours=1)
    fecha_fin = ahora + timedelta(days=1)

    # Categorías necesarias
    muebles, _ = Categoria.objects.get_or_create(nombre="Muebles", defaults={"activa": True})
    vehiculos, _ = Categoria.objects.get_or_create(nombre="Vehículos", defaults={"activa": True})
    arte, _ = Categoria.objects.get_or_create(nombre="Arte", defaults={"activa": True})
    deportes, _ = Categoria.objects.get_or_create(nombre="Deportes", defaults={"activa": True})

    # Anuncios
    anuncio1 = Anuncio.objects.create(
        titulo="Escritorio de oficina",
        descripcion="Escritorio amplio de madera maciza.",
        precio_inicial=100.00,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        activo=True,
        publicado_por=usuario
    )
    anuncio1.categorias.add(muebles)

    anuncio2 = Anuncio.objects.create(
        titulo="Moto Zanella 110cc",
        descripcion="Moto usada, en excelente estado.",
        precio_inicial=300.00,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        activo=True,
        publicado_por=usuario
    )
    anuncio2.categorias.add(vehiculos)

    anuncio3 = Anuncio.objects.create(
        titulo="Cuadro autografiado de Messi",
        descripcion="Edición limitada, con certificado de autenticidad.",
        precio_inicial=1000.00,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        activo=True,
        publicado_por=usuario
    )
    anuncio3.categorias.add(arte)

    anuncio4 = Anuncio.objects.create(
        titulo="Bicicleta de montaña",
        descripcion="Ideal para terrenos difíciles, poco uso.",
        precio_inicial=250.00,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        activo=True,
        publicado_por=usuario
    )
    anuncio4.categorias.add(deportes)

    return anuncio1, anuncio2, anuncio3, anuncio4