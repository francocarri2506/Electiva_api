from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Categoria, Anuncio
from .serializers import CategoriaSerializer, AnuncioSerializer
from ..usuario.models import Usuario


#Vista para listar todas las categorías y crear una nueva:

class CategoriaListaAPIView(APIView):
    def get(self, request, format=None):
        categorias = Categoria.objects.all()  #tengo un queryset de categorias
        serializer = CategoriaSerializer(categorias, many=True) #serializazmos
        return Response(serializer.data) #retornamos y le enviamos el .data que nos devuelve los datos serializados

    def post(self, request, format=None): #mismos parametros para el metodo post
        serializer = CategoriaSerializer(data=request.data) #recibimos los datos y creamos el serializador
        if serializer.is_valid(): #comprobamos si es valido
            serializer.save() #si es valido guardamos
            return Response(serializer.data, status=status.HTTP_201_CREATED) #respuesta de exito
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #respuesta de error

# Vista para obtener, modificar y eliminar una categoria:

class CategoriaDetalleAPIView(APIView):
    def get(self, request, pk, format=None): #tambien va a recibir el la clave primeria que seria el id
        categoria = get_object_or_404(Categoria, pk=pk) #comprobar si existe la categoria y obtengo la instancia
        serializer = CategoriaSerializer(categoria) #la serializo
        return Response(serializer.data) #

    def put(self, request, pk, format=None):
        categoria = get_object_or_404(Categoria, pk=pk)
        serializer = CategoriaSerializer(categoria, data=request.data) #le enviamos tambien la data que proviene de la peticion
        if serializer.is_valid(): #si es valido
            serializer.save() #se modifica el registro de la categoria correspondiente
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #en caso no sea valido se devuelve el error

    def delete(self, request, pk, format=None): #para eliminar
        categoria = get_object_or_404(Categoria, pk=pk) #obtenemos el objeto
        categoria.delete() #lo eliminamos
        return Response(status=status.HTTP_204_NO_CONTENT) #y devolvemos un mensaje de exito


#Vista para listar todos los anuncios y crear una nuevo:

class AnuncioListaAPIView(APIView):
    def get(self, request, format=None):
        anuncios = Anuncio.objects.all()
        serializer = AnuncioSerializer(anuncios, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AnuncioSerializer(data=request.data)
        if serializer.is_valid():
            # Forzamos el usuario publicado_por
            usuario = get_object_or_404(Usuario, pk=1)  # Cambia el ID por el de un usuario válido
            serializer.save(publicado_por=usuario)  #
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
    def post(self, request, format=None):
        data = request.data.copy()

        # Forzar usuario asignado
        data['publicado_por'] = 1

        serializer = AnuncioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""


class AnuncioDetalleAPIView(APIView):
    def get(self, request, pk, format=None): #Define lo que se hace cuando se hace una petición GET al endpoint, por ejemplo: GET /api-view/anuncio/3/ para obtener el anuncio con ID 3.
        anuncio = get_object_or_404(Anuncio, pk=pk) #buscar un anuncio con la clave primaria (pk)
        serializer = AnuncioSerializer(anuncio) #Se serializa el objeto anuncio para convertirlo a un formato JSON válido que se pueda enviar como respuesta al cliente
        return Response(serializer.data) #Se retorna una respuesta HTTP con los datos serializados del anuncio

    def put(self, request, pk, format=None): #Maneja una petición PUT, que en REST implica reemplazar completamente el recurso con los datos nuevos
        anuncio = get_object_or_404(Anuncio, pk=pk)
        serializer = AnuncioSerializer(anuncio, data=request.data)# Se instancia el serializer con el objeto existente (anuncio) y los nuevos datos que llegaron desde el cliente (request.data).
        if serializer.is_valid(): #Verifica si los datos enviados cumplen con las reglas del serializador
            serializer.save() #Si los datos son válidos, se actualiza el objeto anuncio con los nuevos datos.
            return Response(serializer.data) #Devuelve los datos actualizados en la respuesta
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None): #Maneja una petición DELETE al endpoint, por ejemplo: DELETE /api-view/anuncio/3/
        anuncio = get_object_or_404(Anuncio, pk=pk)
        anuncio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) #Devuelve una respuesta sin contenido, con código 204, que indica que la eliminación fue exitosa

    def patch(self, request, pk): #Maneja una petición PATCH, que se usa para actualizar parcialmente un objeto.
        anuncio = get_object_or_404(Anuncio, pk=pk) #pasamos el anuncio actual y los nuevos datos.
        serializer = AnuncioSerializer(anuncio, data=request.data, partial=True) # EL PARTIAL LO QUE NOS PERMITE ES MODIFICAR SOLO UN CAMPO
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)