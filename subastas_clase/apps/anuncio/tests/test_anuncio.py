def test_foo():
    assert True


def test_lista():
    assert list(reversed([1, 2, 3])) == [3, 2, 1]


import pytest
from django.utils import timezone
from datetime import timedelta
from apps.anuncio.models import Anuncio
from .fixtures_user import get_authenticated_client, get_user_generico
from .fixtures_user import get_authenticated_client, get_user_generico, api_client, api_client
from .fixtures_anuncio import categoria_activa, get_anuncios, get_anuncio_modificable
from .conftest import *

#1 Creación de Anuncio

#1.1 Creación correcta de un anuncio verificando sus datos internos
# ( fechas, etc y que el usuario autenticado sea el usuario que publica el anuncio


@pytest.mark.django_db
def test_creacion_correcta_anuncio(get_authenticated_client, categoria_activa):
    cliente = get_authenticated_client

    fecha_inicio = timezone.now() + timedelta(hours=2)
    fecha_fin = fecha_inicio + timedelta(hours=2)

    data = {
        "titulo": "PlayStation 5 en oferta",
        "descripcion": "Consola nueva con garantía",
        "precio_inicial": "500.00",
        "fecha_inicio": fecha_inicio.isoformat(),
        "fecha_fin": fecha_fin.isoformat(),
        "activo": True,
        "categorias": [categoria_activa.nombre]
    }

    response = cliente.post('/api/anuncios/', data, format='json')

    assert response.status_code == 201
    response_data = response.data

    anuncio = Anuncio.objects.get(uuid=response_data['uuid'])

    assert anuncio.titulo == data['titulo']
    assert anuncio.publicado_por.username == 'test_user'
    assert abs(anuncio.fecha_inicio - fecha_inicio) < timedelta(seconds=1)
    assert abs(anuncio.fecha_fin - fecha_fin) < timedelta(seconds=1)
    assert anuncio.activo is True
    assert categoria_activa in anuncio.categorias.all()


#1.2 Creación fallida de un anuncio por datos inválidos

@pytest.mark.django_db
def test_api_creacion_anuncio_precio_falla(get_authenticated_client, categoria_activa):
    client = get_authenticated_client
    ahora = timezone.now()

    data = {
        "titulo": "Artículo sin precio",
        "descripcion": "Este anuncio debería fallar",
        "precio_inicial": "0.00",
        "fecha_inicio": (ahora + timedelta(hours=1)).isoformat(),
        "fecha_fin": (ahora + timedelta(hours=3)).isoformat(),
        "activo": True,
        "categorias": [categoria_activa.nombre]
    }

    response = client.post('/api/anuncios/', data, format='json')
    assert response.status_code == 400
    assert "precio_inicial" in response.data
    assert "mayor a cero" in str(response.data["precio_inicial"][0])

@pytest.mark.django_db
def test_api_creacion_anuncio_fecha_inicio_pasada_falla(get_authenticated_client, categoria_activa):
    client = get_authenticated_client
    ahora = timezone.now()

    data = {
        "titulo": "Fecha pasada",
        "descripcion": "Debería fallar por fecha de inicio",
        "precio_inicial": "100.00",
        "fecha_inicio": (ahora - timedelta(hours=1)).isoformat(),
        "fecha_fin": (ahora + timedelta(hours=3)).isoformat(),
        "activo": True,
        "categorias": [categoria_activa.nombre]
    }

    response = client.post('/api/anuncios/', data, format='json')
    assert response.status_code == 400
    assert "fecha_inicio" in response.data

@pytest.mark.django_db
def test_api_creacion_anuncio_fecha_fin_antes_de_inicio_falla(get_authenticated_client, categoria_activa):
    client = get_authenticated_client
    ahora = timezone.now()

    data = {
        "titulo": "Fin antes que inicio",
        "descripcion": "Debería fallar por lógica de fechas",
        "precio_inicial": "100.00",
        "fecha_inicio": (ahora + timedelta(hours=2)).isoformat(),
        "fecha_fin": (ahora + timedelta(minutes=30)).isoformat(),
        "activo": True,
        "categorias": [categoria_activa.nombre]
    }

    response = client.post('/api/anuncios/', data, format='json')
    assert response.status_code == 400
    assert "fecha_fin" in response.data or "non_field_errors" in response.data



@pytest.mark.django_db
@pytest.mark.parametrize("field, value, expected_msg", [
    ("precio_inicial", "0.00", "El precio inicial debe ser mayor a cero."),
    ("fecha_inicio", (timezone.now() - timedelta(hours=1)).isoformat(), "La fecha de inicio debe ser posterior a la fecha y hora actual."),
    #("fecha_fin", (timezone.now() + timedelta(minutes=30)).isoformat(), "La subasta debe durar al menos 1 hora.")
    ("fecha_fin", (timezone.now() + timedelta(minutes=30)).isoformat(),"La fecha de fin debe ser posterior a la fecha de inicio.")

])

def test_api_creacion_anuncio_datos_invalidos(get_authenticated_client, categoria_activa, field, value, expected_msg):
    client = get_authenticated_client
    ahora = timezone.now()

    # Valores válidos base
    data = {"titulo": "Test Parametrizado", "descripcion": "Probando errores comunes", "precio_inicial": "100.00",
            "fecha_inicio": (ahora + timedelta(hours=2)).isoformat(),
            "fecha_fin": (ahora + timedelta(hours=4)).isoformat(), "activo": True,
            "categorias": [categoria_activa.nombre], field: value}

    # Inyectamos el valor inválido en el campo específico

    response = client.post('/api/anuncios/', data, format='json')
    assert response.status_code == 400

    # El mensaje puede estar en un campo específico o en non_field_errors
    mensaje_error = None

    if field in response.data:
        mensaje_error = str(response.data[field][0])
    elif "non_field_errors" in response.data:
        mensaje_error = str(response.data["non_field_errors"][0])
    else:
        pytest.fail(f"No se encontró el campo de error esperado para {field}")

    assert expected_msg in mensaje_error



#2Modificación de Anuncio


#2.1 Modificación correcta sobre un anuncio verificando sus datos internos ( fechas, etc y que el usuario
# creador del anuncio sea quien modifica el anuncio


@pytest.mark.django_db
def test_api_modificacion_correcta_anuncio(get_authenticated_client, get_anuncio_modificable):
    cliente = get_authenticated_client
    anuncio = get_anuncio_modificable
    usuario = anuncio.publicado_por

    nuevo_titulo = "Xbox Series X - Edición Especial"
    nuevo_precio = 500.00
    nueva_fecha_fin = anuncio.fecha_fin + timedelta(hours=1)

    data = {
        "titulo": nuevo_titulo,
        "precio_inicial": nuevo_precio,
        "fecha_fin": nueva_fecha_fin.isoformat(),
    }
    # lo modifico usando patch ya que no envio todos los datos

    response = cliente.patch(f'/api/anuncios/{anuncio.id}/', data, format='json')
    assert response.status_code == 200

    # verificar que NO se haya modificado el anuncio
    anuncio.refresh_from_db()

    assert anuncio.titulo == nuevo_titulo
    assert anuncio.precio_inicial == nuevo_precio
    assert abs(anuncio.fecha_fin - nueva_fecha_fin) < timedelta(seconds=1)
    assert anuncio.publicado_por == usuario


#2.2 Modificación fallida sobre un anuncio por datos inválidos

@pytest.mark.django_db
def test_api_modificacion_anuncio_falla_datos_invalidos(get_authenticated_client, get_anuncio_modificable):
    client = get_authenticated_client
    anuncio = get_anuncio_modificable

    # Modificación con datos inválidos
    data = {
        "precio_inicial": "0.00",  # inválido
        # "fecha_fin": (fecha_inicio - timedelta(minutes=10)).isoformat()  # antes de inicio
    }

    response = client.patch(f'/api/anuncios/{anuncio.id}/', data, format='json')

    assert response.status_code == 400
    assert "precio_inicial" in response.data
    assert response.data["precio_inicial"][0] == "El precio inicial debe ser mayor a cero."
    # assert "fecha_fin" in response.data or "non_field_errors" in response.data

#2.3 Modificación fallida sobre un anuncio por no coincidir usuario autenticado con usuario creador del anuncio


@pytest.mark.django_db
def test_api_modificacion_anuncio_falla_por_usuario_incorrecto(api_client, django_user_model, categoria_activa):

    user_a = django_user_model.objects.create_user(
        username="dueño",
        password="test1234",
        documento_identidad="12345678"
    )

    user_b = django_user_model.objects.create_user(
        username="intruso",
        password="test1234",
        documento_identidad="87654321"
    )

    # el primer usuario va a crear un anuncio
    fecha_inicio = timezone.now() + timedelta(hours=2)
    fecha_fin = fecha_inicio + timedelta(hours=2)

    anuncio = Anuncio.objects.create(
        titulo="samsung a32",
        descripcion="Anuncio de prueba",
        precio_inicial=1500.00,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        activo=True,
        publicado_por=user_a
    )
    anuncio.categorias.add(categoria_activa)


    # me registro con el usuario que no tendria permisos de modificacion
    client = api_client
    client.force_authenticate(user=user_b)

    # intento modificar solo el nombre para probar
    data = {
        "titulo": "samsung a32 premium"
    }

    response = client.patch(f'/api/anuncios/{anuncio.id}/', data, format='json')

    assert response.status_code == 403
    assert response.data['detail'] == "Solo el creador del anuncio puede modificarlo."


@pytest.mark.django_db
def test_api_modificacion_anuncio_falla_por_usuario_incorrecto(api_client, usuario_intruso, anuncio_de_otro_usuario):
    anuncio = anuncio_de_otro_usuario

    client = api_client
    client.force_authenticate(user=usuario_intruso)

    data = {
        "titulo": "Samsung A32 Premium"
    }

    response = client.patch(f'/api/anuncios/{anuncio.id}/', data, format='json')

    assert response.status_code == 403
    assert response.data['detail'] == "Solo el creador del anuncio puede modificarlo."


#3 Listado de Anuncios

# 3.1 Listado completo de anuncios


@pytest.mark.django_db
def test_api_listado_completo_anuncios(get_authenticated_client, get_anuncios):
    cliente = get_authenticated_client
    anuncio1, anuncio2, anuncio3, anuncio4 = get_anuncios

    response = cliente.get('/api/anuncios/')

    assert response.status_code == 200
    # #data = response.data
    data = response.data['results'] #el error es porque estoy usando DRF con paginación activada

    assert data[0]['titulo'] == anuncio1.titulo # Escritorio
    assert data[1]['titulo'] == anuncio2.titulo # Moto
    assert data[2]['titulo'] == anuncio3.titulo  # Cuadro Messi
    assert data[3]['titulo'] == anuncio4.titulo  # Bicicleta


# 3.2 Listado de anuncios aplicando filtros

@pytest.mark.django_db
def test_api_listado_anuncios_filtrados_por_categoria(get_authenticated_client, get_anuncios):
    cliente = get_authenticated_client
    anuncio1, anuncio2, anuncio3, anuncio4 = get_anuncios

    # Filtro por categoría: "Vehículos" (Moto)
    response = cliente.get('/api/anuncios/?categorias=Vehículos')

    assert response.status_code == 200
    data = response.data['results']

    assert len(data) == 1
    assert data[0]['titulo'] == anuncio2.titulo


