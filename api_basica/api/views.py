from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Base de datos en memoria (simulación)

items = [{"id": 1, "nombre": "Laptop"}, {"id": 2, "nombre": "Telefono"}]


@csrf_exempt  # Desactiva la verificación CSRF para pruebas
def obtener_agregar_items(request):
    if request.method == 'GET':  # Devolver la lista de ítems en formato JSON
        return JsonResponse(items, safe=False) #le decimos que no le mandamos un diccionario sino una lista con diccionarios
    elif request.method == 'POST': #nos envian los datos para agregar un nuevo producto
        try:
            data = json.loads(request.body)  # Convertir JSON en diccionario
            nuevo_item = {"id": len(items) + 1,
                          "nombre": data.get("nombre", "Sin nombre")} #si no trae nombre pongo sin nombre
            items.append(nuevo_item)  # Agregar el nuevo ítem creado a la lista
            return JsonResponse(nuevo_item, status=201)  # Respuesta
        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato JSON inválido"}, status=400) #codigo de estado 400


@csrf_exempt
def modificar_eliminar_item(request, item_id):
    item = next((item for item in items if item["id"] == item_id), None)

    if item is None:
        return JsonResponse({"error": "Ítem no encontrado"}, status=404)

    if request.method == 'PUT': #para modificar el item seleccionado
        try:
            data = json.loads(request.body)
            item["nombre"] = data.get("nombre", item["nombre"])
            return JsonResponse(item)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato JSON inválido"}, status=400)

    elif request.method == 'DELETE': #para eliminar el item selecionado
        items.remove(item)
        return JsonResponse({"mensaje": "Ítem eliminado"}, status=200)