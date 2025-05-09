from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import CategoriaFilter, AnuncioFilter
from .models import Categoria, Anuncio
from .serializers import CategoriaSerializer, AnuncioSerializer, OfertaAnuncioSerializer
from ..usuario.models import Usuario


#Vista para listar todas las categorías y crear una nueva:
"""
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
"""

 ######para solucionar el error cuando estaba probando desde postman

from rest_framework.views import APIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import status
from apps.anuncio.models import Categoria
from apps.anuncio.serializers import CategoriaSerializer

class CategoriaListaAPIView(APIView):
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Categoria.objects.all()

    def get(self, request, format=None):
        categorias = self.get_queryset()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
"""
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




#------------------------------- esto lo comento para el tp5 desde linea 100 a linea 165-----------------------------------

#Se elimina código redundante.

#Se respetan correctamente los permisos del sistema.

#Se mantiene el comportamiento esperado para GET, PUT, PATCH y DELETE.
"""  """

#me estaba dando error la parte de arriba
from rest_framework import generics, permissions

class AnuncioListaAPIView(generics.ListCreateAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def perform_create(self, serializer):
        usuario = get_object_or_404(Usuario, pk=1)  # o usar request.user si ya hay autenticación
        serializer.save(publicado_por=usuario)

"""   """
#esto estaba comentado desde antes del tp5
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
""" """


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
        if serializer.is_valid(): #aca se aplican todas las validaciones y se convoca a save
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    #Vista Concreta para listar y crear Categorias (ListCreateAPIView) y Vista Concreta para
    #recuperar, actualizar y eliminar una categoria (RetrieveUpdateDestroyAPIView):

""" """


from rest_framework.generics import (get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from .models import Categoria
from .serializers import CategoriaSerializer


class CategoriaListaGenericView(ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class CategoriaDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


#ViewSet: ModelViewSet y ReadOnlyModelViewSet

from rest_framework import viewsets
""" #comentado para hacer lo del tp4 que es la parte de abajo
class CategoriaViewSet(viewsets.ModelViewSet): #La clase ModelViewSet, proporciona todas las acciones, para listar, recuperar, crear y eliminar objetos correspondientes a un Modelo definido.
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
"""
####### para el tp4 DEFINICION DE FILTROS Y ORDEN EN EL API ######
"""
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    def get_queryset(self):
        return Categoria.objects.filter(nombre__istartswith='a') #solo categorias que empiezan con a
"""

#--------- no me estaria funcionando, no muestra nada------------------
"""
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    def get_queryset(self):
        queryset = Categoria.objects.all() #si no paso un nombre por parametro me devuelve todo
        parametro_nombre = self.request.query_params.get('nombre', None)
        if parametro_nombre is not None:
           # queryset = queryset.filter(nombre=parametro_nombre) #se pueden filtros por igualdad
           queryset = queryset.filter(nombre__icontains=parametro_nombre)
        return queryset
"""
######################### USO DE DJANGO FILTER BACKEND  #########################
"""
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    #filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre', 'activa']

"""

######################### USO DE DJANGO FILTER BACKEND luego de crear el archivo filters.py #########################
"""
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filterset_class = CategoriaFilter
"""
######################### USO DE ORDERING FILTER  #########################

from rest_framework import status, viewsets, filters

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CategoriaFilter
    ordering_fields = ['nombre', 'activa'] #campos por los cuales puedo ordenar
    ordering = ['nombre'] #orden por defecto
#-------------------------------vistas genéricas (GenericView)-----------------------------------

#------------------------- vista para listar y crear anuncios ----------

class AnuncioListaGenericView(ListCreateAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer

    def perform_create(self, serializer):
        # Asignamos el usuario autenticado como "publicado_por"
        serializer.save(publicado_por=self.request.user)

#------------------------- vista para ver, actualizar o eliminar un anuncio---------------

class AnuncioDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer







#------------------------------- usando ViewSets-----------------------------------

#ModelViewSet incluye todas las operaciones CRUD automáticamente

#-----------------------------------------------------------------------------------

from rest_framework.decorators import action
from datetime import datetime, timezone as dt_timezone
from rest_framework.permissions import IsAuthenticated



from rest_framework.permissions import DjangoObjectPermissions

from rest_framework.permissions import IsAuthenticatedOrReadOnly
#from apps.anuncio.permissions import EsDueñoOsoloLectura


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class AnuncioViewSet(viewsets.ModelViewSet):
    queryset = Anuncio.objects.all() # que datos son los que nesesito
    serializer_class = AnuncioSerializer # que serializador voy a usar


#con esto ya me muestra desde postman pero no desde la URL

    #cuando nesesito modificar lo que esta en el seting recien debo agregar estos campos

    authentication_classes = [TokenAuthentication]
    permission_classes = [DjangoModelPermissions]


    """  
    #permission_classes = [IsAuthenticated] #para el punto2
    #permission_classes = [IsAuthenticated, DjangoObjectPermissions] #Esto activa la verificación de permisos a nivel de objeto (para editar/eliminar).
    #permission_classes = [IsAuthenticatedOrReadOnly, EsDueñoOsoloLectura] #verificacion personalizada para eliminar y modificar
    """


#----------------------------     filtros y orden   ----------------------------------------------------------

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    #filterset_fields = ['activo', 'publicado_por', 'categorias']  # Filtrar por estos campos
    filterset_class = AnuncioFilter
    ordering_fields = ['fecha_inicio', 'precio_inicial', 'fecha_fin']  # Ordenar por estos campos
    search_fields = ['titulo', 'descripcion']  # Buscar por texto

#--------------------------------------------------------------------------------------------------------------

    #Sobrescribimos este método para que automáticamente se asigne el usuario autenticado
    def perform_create(self, serializer):
        serializer.save(publicado_por=self.request.user)


    @action(detail=True, methods=['get']) #con detail=true para aplicar esta accion  a un objeto específico el que este seleccionado
    def tiempo_restante(self, request, pk=None):
        anuncio = self.get_object()
        if anuncio.fecha_fin: #verificamos que tenga una fecha de fin
            ahora = datetime.now(dt_timezone.utc) #nesesito la hora actual
            calculado = anuncio.fecha_fin - ahora #calculamos el tiempo en dias,segundos y minutos
            if calculado.total_seconds() > 0:
                dias = calculado.days
                horas = calculado.seconds // 3600
                minutos = (calculado.seconds % 3600) // 60
                return Response({
                    'dias': dias,
                    'horas': horas,
                    'minutos': minutos
                })
            else:
                return Response({'mensaje': 'El anuncio ya ha finalizado.'}) #Si el tiempo ya pasó
        return Response({'mensaje': 'Este anuncio no tiene fecha de finalización.'}) #si la fecha es igual a null

    @action(detail=True, methods=['post'], url_path='ofertar')
    def ofertar(self, request, pk=None):
        anuncio = self.get_object()

#agregar codigos mas precisos

        if not anuncio.activo:
            return Response({"error": "El anuncio ya no está activo."}, status=status.HTTP_400_BAD_REQUEST)

        if anuncio.publicado_por == request.user:
            return Response({"error": "No puedes ofertar en tu propio anuncio."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OfertaAnuncioSerializer(data=request.data)
        if serializer.is_valid():
            try:
                oferta = serializer.save(usuario=request.user, anuncio=anuncio)
                return Response (serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


 ###################orden y filtro para categoria yo
"""
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['nombre']
    ordering_fields = ['nombre']
    search_fields = ['nombre']

"""





"""
###########  Ejemplo de Acción personalizada con ViewSet  ##########

from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UserSerializer, PasswordSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    #Una acción específica para modificar el password de un Usuario (detail=True) 
    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        # Se obtiene la instancia de Usuario de acuerdo al ‘pk’ enviado en la url
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""







"""

#--------------------para el tp5 correcciones---------------------------

from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import AnuncioSerializer

class AnuncioListaAPIView(generics.ListCreateAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def perform_create(self, serializer):
        usuario = get_object_or_404(Usuario, pk=1)  # o usar request.user si ya hay autenticación
        serializer.save(publicado_por=usuario)


class AnuncioDetalleAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer
    permission_classes = [permissions.DjangoModelPermissions]


"""



#"detail": "Method \"GET\" not allowed."
#significa que estás accediendo a la URL correcta, pero usando el método GET, y este endpoint está definido solo para POST.