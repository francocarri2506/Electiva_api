import pytest
from rest_framework.test import APIClient
from apps.anuncio.models import OfertaAnuncio
from django.contrib.auth import get_user_model
from .fixtures_oferta import get_anuncio_para_oferta,get_usuario_ofertante




# 4Creación de Oferta sobre Anuncio


# 4.1 Creación correcta de una Oferta de Anuncio verificando que los datos sean validos, que el usuario ofertante
# sea diferente al creador de un anuncio y verificando que el anuncio se encuentre activo al momento de la oferta

@pytest.mark.django_db
def test_api_creacion_oferta_correcta(get_anuncio_para_oferta, get_usuario_ofertante):
    anuncio = get_anuncio_para_oferta
    creador = anuncio.publicado_por
    ofertante = get_usuario_ofertante

    client = APIClient()
    client.force_authenticate(user=ofertante)

    data = {
        "precio_oferta": "850.00"
    }

    response = client.post(f'/api/anuncios/{anuncio.id}/ofertar/', data, format='json')

    assert response.status_code == 201

    # Validamos contenido
    assert response.data['precio_oferta'] == "850.00"

    # Validamos en base de datos
    oferta = OfertaAnuncio.objects.get(usuario=ofertante, anuncio=anuncio)
    assert oferta.precio_oferta == 850.00
    assert oferta.anuncio == anuncio
    assert oferta.usuario == ofertante

# 4.2 Creación fallida de una Oferta de Anuncio por contener datos inválidos


@pytest.mark.django_db
def test_api_creacion_oferta_falla_por_precio_bajo(get_anuncio_para_oferta, get_usuario_ofertante):
    anuncio = get_anuncio_para_oferta
    ofertante = get_usuario_ofertante

    client = APIClient()
    client.force_authenticate(user=ofertante)

    # Precio igual al inicial (800), no válido
    data = {
        "precio_oferta": "800.00"
    }

    response = client.post(f'/api/anuncios/{anuncio.id}/ofertar/', data, format='json')

    assert response.status_code == 400
    assert "error" in response.data
    assert response.data["error"] == "La oferta debe ser mayor al precio inicial del artículo."


# 4.3 Creación fallida de una Oferta de Anuncio porque el usuario que intenta ofertar es el creador del mismo
# anuncio


@pytest.mark.django_db
def test_api_oferta_falla_si_usuario_es_creador(get_anuncio_para_oferta):
    anuncio = get_anuncio_para_oferta
    creador = anuncio.publicado_por

    cliente = APIClient()
    cliente.force_authenticate(user=creador)

    data = {
        "precio_oferta": "850.00"
    }

    response = cliente.post(f'/api/anuncios/{anuncio.id}/ofertar/', data, format='json')

    assert response.status_code == 400
    assert "error" in response.data
    assert response.data["error"] == "No puedes ofertar en tu propio anuncio."