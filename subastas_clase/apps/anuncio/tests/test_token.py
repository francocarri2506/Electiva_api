import pytest
from .fixtures_user import api_client, create_user, crear_token_usuario

from django.urls import reverse

@pytest.mark.django_db
def test_obtener_token_valido(api_client):
    # crear un usuario
    usuario = create_user(username='nuevo_user', password='fif555', documento_identidad='45785965')

    # No es necesario crear un token manualmente ya que el endpoint "/api-token-auth/" de "rest_framework.authtoken"
    # lo genera automáticamente al autenticar correctamente al usuario.

    # Tener en cuenta que se debe enviar la contraseña en texto plano, porque el valor devuelto por "usuario.password"
    # devuelve una contraseña hasheada que no se puede “desencriptar”.


    #usar reverse() para evitar hardcodear la URL

    url = reverse('api-token-auth')
    response = api_client.post(url, data={
        'username': usuario.username,
        'password': 'fif555'
    })

    #para mi url

    # response = api_client.post('/api/token-auth/', data={
    #     'username': usuario.username,
    #     'password': 'fif555'
    # })

    #como lo tenia la profe

    # response = api_client.post('/api-token-auth/', data={
    #     'username': usuario.username,
    #     'password': 'fif555'
    # })

    assert response.status_code == 200
    assert 'token' in response.data
