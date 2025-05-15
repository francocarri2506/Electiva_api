
import requests
from django.http import JsonResponse

"""
def obtener_tasa_cambio(moneda_destino='USD'):
    try:
        #url = 'https://open.er-api.com/v6/latest/ARS' #gratuita sin registro
        url ='https://v6.exchangerate-api.com/v6/b193f15b2ce8dde33a75669e/latest/ARS' #registrandome, con api key b193f15b2ce8dde33a75669e

        response = requests.get(url, timeout=5)
        data = response.json()
        return data['rates'].get(moneda_destino, None)
    except Exception as e:
        print(f"Error al obtener la tasa de cambio: {e}")
        return None

"""


def obtener_tasa_cambio(moneda_destino='USD'):
    try:
        api_key = 'b193f15b2ce8dde33a75669e' #guardar en un archivo de entorno
        url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/ARS'
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Lanza excepción para errores HTTP (4xx/5xx)

        data = response.json()

        if data.get("result") != "success":
            print(f"Error de API: {data.get('error-type')}")
            return None

        return data['conversion_rates'].get(moneda_destino, None)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err}")
        return JsonResponse({"error": "Hubo un problema al consultar el servicio externo."}, status=502)

    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error: {conn_err}")
        return JsonResponse({"error": "No se pudo conectar al servicio externo. Inténtelo más tarde."}, status=503)

    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error: {timeout_err}")
        return JsonResponse({"error": "El servicio externo tardó demasiado en responder."}, status=504)

    except requests.exceptions.RequestException as err:
        print(f"Request error: {err}")
        return JsonResponse({"error": "Ocurrió un error inesperado al contactar el servicio externo."}, status=500)