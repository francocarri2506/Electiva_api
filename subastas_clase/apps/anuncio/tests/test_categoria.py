import pytest
from .fixtures_user import get_authenticated_client, get_user_generico, api_client, api_client
from .fixtures_categoria import get_categorias
from ..models import Categoria


@pytest.mark.django_db
def test_api_lista_categorias(get_authenticated_client, get_categorias):
    cliente = get_authenticated_client

    categoria1, categoria2, categoria3 = get_categorias
    #response = cliente.get('/view-set/categoria/') #yo
    response = cliente.get(f'/api/categoria/')
    assert response.status_code == 200

    # verificar que se devuelvan las categorias creadas en "get_categorias"
    # tener en cuenta que puede variar el orden de las categorias devueltas en funcion de los parametros iniciales del api

    #data = response.data
    data = response.data['results']
    assert data[0]['nombre'] == categoria1.nombre # Computacion
    assert data[1]['nombre'] == categoria2.nombre  # Electronica
    assert data[2]['nombre'] == categoria3.nombre  # Hogar


@pytest.mark.django_db
def test_api_lista_categorias_filtradas(get_authenticated_client, get_categorias):
    cliente = get_authenticated_client

    categoria1, categoria2, categoria3 = get_categorias

    # se comprueba que la categoria3 está inactiva", por lo cual quedan solo dos categorias activas
    assert categoria1.activa
    assert categoria2.activa
    assert not categoria3.activa

    response = cliente.get(f'/api/categoria/?activa=true')
    assert response.status_code == 200

    # verificar que se devuelvan solo las dos categorias activas

    #data = response.data
    data = response.data['results']
    assert len(data) == 2
    assert data[0]['nombre'] == categoria1.nombre # Computacion
    assert data[1]['nombre'] == categoria2.nombre  # Electronica


@pytest.mark.django_db
def test_api_lista_categorias_falla_usuario_no_autenticado(api_client, get_categorias):
    response = api_client.get(f'/api/categoria/')

    assert response.status_code == 401
    assert str(response.data['detail']) == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_api_creacion_categoria(get_authenticated_client, get_categorias):
    client = get_authenticated_client

    data = {
        "nombre": "Indumentaria",
    }

    response = client.post(f'/api/categoria/', data=data)
    #response = client.post('/view-set/categoria/', data=data)
    assert response.status_code == 201
    assert Categoria.objects.filter(nombre='Indumentaria').count() == 1


@pytest.mark.django_db
def test_api_creacion_categoria_repetida_falla(get_authenticated_client, get_categorias):
    client = get_authenticated_client

    categoria1, categoria2, categoria3 = get_categorias
    assert categoria3.nombre == 'Hogar'

    data = {
        "nombre": "Hogar",
    }

    # Se intenta crear una categoria con un nombre existente
    response = client.post(f'/api/categoria/', data=data)
    assert response.status_code == 400
    assert str(response.data['nombre'][0]) == 'categoria with this nombre already exists.'
    assert Categoria.objects.filter(nombre='Hogar').count() == 1


@pytest.mark.django_db
def test_api_creacion_categoria_falla(get_authenticated_client):
    client = get_authenticated_client

    data = {
        "nombre": "Categoria Hogar",
    }

    # Se intenta crear una categoria que contiene la "categoria" en el nombre
    response = client.post(f'/api/categoria/', data=data)
    assert response.status_code == 400
    #assert str(response.data['nombre'][0]) == "El nombre no puede contener la palabra 'categoria'."
    assert str(response.data['nombre'][0]) == "El nombre no puede contener la palabra 'categoría'."
    assert not Categoria.objects.filter(nombre__icontains='Categoria Hogar').exists()


@pytest.mark.django_db
def test_api_modificacion_categoria(get_authenticated_client, get_categorias):
    client = get_authenticated_client

    categoria1, categoria2, categoria3 = get_categorias
    assert categoria3.nombre == 'Hogar'

    data = {
        "nombre": "Hogar y Bazar",
    }

    response = client.patch(f'/api/categoria/{categoria3.id}/', data=data)
    assert response.status_code == 200
    assert response.data['id'] == categoria3.id
    assert response.data['nombre'] == 'Hogar y Bazar'

    categoria3.refresh_from_db()
    assert categoria3.nombre == 'Hogar y Bazar'


@pytest.mark.django_db
def test_api_modificacion_categoria_repetida_falla(get_authenticated_client, get_categorias):
    client = get_authenticated_client

    categoria1, categoria2, categoria3 = get_categorias
    assert categoria1.nombre == 'Computacion'
    assert categoria3.nombre == 'Hogar'

    data = {
        "nombre": "Computacion",
    }

    # se intenta modificar el nombre de categoria 3, colocando el mismo nombre de la categoria1
    response = client.patch(f'/api/categoria/{categoria3.id}/', data=data)
    assert response.status_code == 400
    assert str(response.data['nombre'][0]) == 'categoria with this nombre already exists.'

    # verificar que NO se haya modificado la categoria 3
    categoria3.refresh_from_db()
    assert categoria3.nombre == 'Hogar'
