import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.authtoken.models import Token

from apps.anuncio.models import Categoria

User = get_user_model()


# def create_user(username, documento_identidad, first_name='Micaela', last_name='Salgado', password='unpassword', email=None, *, is_active=True):
#     email = '{}@root.com'.format(username) if email is None else email
#
#     user, created = User.objects.get_or_create(username=username, email=email)
#
#     if created:
#         user.documento_identidad = documento_identidad
#         user.first_name = first_name
#         user.last_name = last_name
#         user.is_active = is_active
#         user.set_password(password)  # Se Hashea la contraseña al guardarla en la BD
#         user.save()
#
#     return user

def create_user(username, documento_identidad, first_name='Micaela', last_name='Salgado', password='unpassword', email=None, *, is_active=True, is_staff=False):
    email = '{}@root.com'.format(username) if email is None else email

    user, created = User.objects.get_or_create(username=username, email=email)

    if created:
        user.documento_identidad = documento_identidad
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = is_active
        user.is_staff = is_staff
        user.set_password(password)
        user.save()

    return user


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

#
# @pytest.fixture
# def get_user_generico():
#     test_user = create_user(username='test_user', documento_identidad='44635875', first_name='Test', last_name='User', email='test@user.com')
#     return test_user

@pytest.fixture
def get_user_generico():
    test_user = create_user(
        username='test_user',
        documento_identidad='44635875',
        first_name='Test',
        last_name='User',
        email='test@user.com',
        is_staff=True
    )

    # Agregar permisos del modelo Categoria
    content_type = ContentType.objects.get_for_model(Categoria)
    permissions = Permission.objects.filter(content_type=content_type, codename__in=[
        'add_categoria', 'change_categoria', 'delete_categoria', 'view_categoria'
    ])
    test_user.user_permissions.set(permissions)

    return test_user


@pytest.fixture
def get_authenticated_client(get_user_generico, api_client):
    token, _ = Token.objects.get_or_create(user=get_user_generico)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return api_client


def get_auth_token(username, password, api_client):
    response = api_client.post('/api-token-auth/', data={
        'username': username,
        'password': password
    })
    assert response.status_code == 200
    return response.data['token']


def crear_token_usuario(usuario):
    token, _ = Token.objects.get_or_create(user=usuario)
    return token

