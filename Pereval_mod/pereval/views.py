import django_filters
from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import *
from .models import *


# передача представлений для API, в соответствии с моделью
class UsersViewset(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['fam', 'name', 'otc', 'email']


class CoordsViewset(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer


class LevelViewset(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImagesViewset(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


# главное представление PerevalsViewset позволяет также создавать и обновлять данные о перевле
class PerevalsViewset(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalsSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['beauty_title', 'title', 'add_time', 'user__email']

    def create(self, request,  *args, **kwargs):  # метод зоздания данных о перевале
        if self.action == 'create':
            serializer = PerevalsSerializer(data=request.data)

            if serializer.is_valid():  # в зависимости от данных, пользователя оповестять о результате операции
                serializer.save()
                return Response(
                    {
                        'status': status.HTTP_200_OK,
                        'message': 'Успешно',
                        'id': serializer.instance.pk,
                    }
                )

            if status.HTTP_400_BAD_REQUEST:
                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Некорректный запрос',
                        'id': None,
                    }
                )

            if status.HTTP_500_INTERNAL_SERVER_ERROR:
                return Response(
                    {
                        'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'message': 'Ошибка при выполнении операции',
                        'id': None,
                    }
                )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):  # метод обновления данных, если данные валидны, то возможно изменение
        if self.action == 'update':
            instance = self.get_object()
            serializer = PerevalsUpdateSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                serializer.save()

                validated_data['state'] = serializer.instance.state
                validated_data['message'] = serializer.instance.message

                return Response(validated_data)

        return super().partial_update(request, *args, **kwargs)

    def get_serializer_class(self):  # отдельный метод завершения - получение обновленного перевала
        if self.action == 'update':
            return PerevalsUpdateSerializer
        return super().get_serializer_class()
