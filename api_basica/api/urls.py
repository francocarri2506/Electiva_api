from django.urls import path
from .views import obtener_agregar_items, modificar_eliminar_item

urlpatterns = [
    path('items/', obtener_agregar_items, name='obtener_agregar_items'),#como la vista es la misma y solo cambia el metodo podemos usar la misma url
    path('items/<int:item_id>/', modificar_eliminar_item, name='modificar_eliminar_item'),
]