from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from apps.anuncio.api.filters import CategoriaFilter, AnuncioFilter
from apps.anuncio.models import Anuncio
from apps.anuncio.api.serializers import AnuncioSerializer, OfertaAnuncioSerializer
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import generics, permissions

from rest_framework.generics import (get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from apps.anuncio.models import Categoria
from apps.anuncio.api.serializers import CategoriaSerializer


from rest_framework import viewsets, filters
from rest_framework.decorators import action
from datetime import datetime, timezone as dt_timezone

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from apps.anuncio.api.permissions import EsCreadorDelAnuncio
from rest_framework.exceptions import PermissionDenied

from uuid import UUID
from rest_framework.exceptions import NotFound, ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError

# -------------------------- API VIEW   ------------------------------------

#Vista para listar todas las categorías y crear una nueva

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


class AnuncioListaAPIView(generics.ListCreateAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def perform_create(self, serializer):
        #usuario = get_object_or_404(Usuario, pk=1)  # o usar request.user si ya hay autenticación
        #serializer.save(publicado_por=usuario)
        serializer.save(publicado_por=self.request.user)

# Vista para obtener, modificar y eliminar un anuncio:

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


    # -------------------------- GenericView  vistas genericas ------------------------------------

    #Vista Concreta para listar y crear Categorias (ListCreateAPIView) y Vista Concreta para
    #recuperar, actualizar y eliminar una categoria (RetrieveUpdateDestroyAPIView):

class CategoriaListaGenericView(ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriaDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

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




#------------------------------- usando ViewSets-----------------------------------

#ModelViewSet incluye todas las operaciones CRUD automáticamente
#ViewSet: ModelViewSet y ReadOnlyModelViewSet

#-----------------------------------------------------------------------------------

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CategoriaFilter
    ordering_fields = ['nombre', 'activa'] #campos por los cuales puedo ordenar
    ordering = ['nombre'] #orden por defecto



class AnuncioViewSet(viewsets.ModelViewSet):

    #lookup_field = 'id' #si agrego el uuid remplazando el id existente
    #lookup_field = 'uuid'

    queryset = Anuncio.objects.all() # que datos son los que nesesito
    serializer_class = AnuncioSerializer # que serializador voy a usar

    #permission_classes = [IsAuthenticated, EsDueñoOsoloLectura]
#----------------------------     filtros y orden   ----------------------------------------------------------

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    #filterset_fields = ['activo', 'publicado_por', 'categorias']  # Filtrar por estos campos
    filterset_class = AnuncioFilter
    ordering_fields = ['fecha_inicio', 'precio_inicial', 'fecha_fin']  # Ordenar por estos campos
    search_fields = ['titulo', 'descripcion']  # Buscar por texto

#--------------------------------------------------------------------------------------------------------------

    """
    # mas persolinalizado que el perform
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), EsDueñoDelAnuncio()]
        return [IsAuthenticated()]
    """
    permission_classes = [IsAuthenticatedOrReadOnly, EsCreadorDelAnuncio]

    #Sobrescribimos este método para que automáticamente se asigne el usuario autenticado
    def perform_create(self, serializer):
        serializer.save(publicado_por=self.request.user)

    #verificar que el usuario sea el dueño al actualizar
    def perform_update(self, serializer):
        anuncio = self.get_object()
        if anuncio.publicado_por != self.request.user:
            raise PermissionDenied("Solo el creador del anuncio puede modificarlo.")
        serializer.save()

    # verificar que el usuario sea el dueño al eliminar
    def perform_destroy(self, instance):
        if instance.publicado_por != self.request.user:
            raise PermissionDenied("Solo el creador del anuncio puede eliminarlo.")
        instance.delete()


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
            return Response({"error": "El anuncio ya no se encuentra activo."}, status=status.HTTP_400_BAD_REQUEST)

        if anuncio.publicado_por == request.user:
            return Response({"error": "No puedes ofertar en tu propio anuncio."}, status=status.HTTP_400_BAD_REQUEST)

        # Creamos la oferta

        # serializer = OfertaAnuncioSerializer(data=request.data)
        # if serializer.is_valid():
        #     try:
        #         oferta = serializer.save(usuario=request.user, anuncio=anuncio)
        #         return Response (serializer.data, status=status.HTTP_201_CREATED)
        #
        #     except ValidationError as e:
        #         #return Response({"error": e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
        #         return Response({"error": "La oferta debe ser mayor al precio inicial del artículo."}, status=status.HTTP_400_BAD_REQUEST)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        #para que funcione el test, ya que estaria tomando el valor del clean() para el error y no el de aca

        serializer = OfertaAnuncioSerializer(data=request.data)
        if serializer.is_valid():
            try:
                oferta = serializer.save(usuario=request.user, anuncio=anuncio)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except DjangoValidationError as e:
                return Response({"error": str(e.messages[0])}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    def get_object(self):
        lookup_value = self.kwargs.get(self.lookup_url_kwarg or self.lookup_field)

        try:
            # Intentamos parsear el valor como UUID v4
            uuid_obj = UUID(lookup_value, version=4)
            return self.queryset.get(uuid=uuid_obj)

        except (ValueError, Anuncio.DoesNotExist):
            # Si el UUID es inválido o no existe, intentamos por ID
            try:
                # Verificamos si el lookup_value es un número entero
                if lookup_value.isdigit():
                    return self.queryset.get(id=int(lookup_value))
                else:
                    raise ValidationError({"detalle": "El identificador no es un UUID válido ni un ID numérico."})
            except Anuncio.DoesNotExist:
                raise NotFound("Anuncio no encontrado por ID ni UUID.")
    """

    def get_object(self):
        lookup_value = self.kwargs.get(self.lookup_url_kwarg or self.lookup_field)

        try:
            uuid_obj = UUID(lookup_value, version=4)
            return self.queryset.get(uuid=uuid_obj)

        except (ValueError, Anuncio.DoesNotExist):
            if lookup_value.isdigit():
                try:
                    return self.queryset.get(id=int(lookup_value))
                except Anuncio.DoesNotExist:
                    raise NotFound("No se encontró un anuncio con ese ID.")
            raise ValidationError({"detalle": "El identificador no es un UUID válido ni un ID numérico."})

    """    
        # Creamos la oferta
        serializer = OfertaAnuncioSerializer(data=request.data)
        if serializer.is_valid():
            oferta = serializer.save(usuario=request.user, anuncio=anuncio)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "La oferta debe ser mayor al precio inicial del artículo"}, status=status.HTTP_400_BAD_REQUEST)
  
    """

    """

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def ofertar(self, request, pk=None):
        anuncio = self.get_object()
        usuario = request.user

        # Validación: no permitir ofertar en propio anuncio
        if anuncio.publicado_por == usuario:
            return Response({"detail": "No puedes ofertar en tu propio anuncio."}, status=status.HTTP_403_FORBIDDEN)

        # Validación: anuncio debe estar activo
        if not anuncio.activo:
            return Response({"detail": "No se puede ofertar en un anuncio inactivo."},
                            status=status.HTTP_400_BAD_REQUEST)


        # Cargamos el serializer con los datos y validamos
        serializer = OfertaAnuncioSerializer(data=request.data)
        if serializer.is_valid():
            try:
                oferta = OfertaAnuncio(
                    anuncio=anuncio,
                    usuario=usuario,
                    precio_oferta=serializer.validated_data['precio_oferta']
                )
                oferta.full_clean()  # Ejecuta el método clean() del modelo
                oferta.save()

                # Devolvemos los datos usando el serializer original
                response_serializer = OfertaAnuncioSerializer(oferta)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

            except ValidationError as e:
                return Response({'detail': e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
    """




    """ #probar luego de documentar
    lookup_field = 'uuid'  # Establecemos UUID como campo por defecto para búsqueda

    def get_object(self):
        lookup_value = self.kwargs.get(self.lookup_url_kwarg or self.lookup_field)

        try:
            # Si es un UUID válido, buscar por UUID
            uuid_obj = UUID(lookup_value, version=4)
            return self.queryset.get(uuid=uuid_obj)

        except (ValueError, Anuncio.DoesNotExist):
            # Si no es UUID, intentar como ID numérico
            if lookup_value.isdigit():
                try:
                    return self.queryset.get(id=int(lookup_value))
                except Anuncio.DoesNotExist:
                    raise NotFound("No se encontró un anuncio con ese ID.")
            # Si no es UUID ni ID válido
            raise ValidationError({"detalle": "El identificador no es un UUID válido ni un ID numérico."})
    """
