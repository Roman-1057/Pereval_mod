from .models import *
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from drf_writable_nested import WritableNestedModelSerializer


# ниже представлены классы сериалайзеров для моделей
class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['fam', 'name', 'otc', 'email', 'phone']


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['summer', 'autumn', 'winter', 'spring']


class ImagesSerializer(serializers.ModelSerializer):
    image = serializers.URLField()
    date_added = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Images
        fields = ['title', 'date_added', 'image']


class PerevalsSerializer(WritableNestedModelSerializer):
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    user = UsersSerializer()
    coord = CoordsSerializer()
    level = LevelSerializer()
    images = ImagesSerializer(many=True, required=False)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Pereval
        fields = ['beauty_title',
                  'title',
                  'other_titles',
                  'connect',
                  'status',
                  'add_time',
                  'level',
                  'user',
                  'coord',
                  'images'
                  ]


# сериалайзер PerevalsUpdateSerializer включает в себя работу предыдущих сериалайзеры, для связи с данными
class PerevalsUpdateSerializer(WritableNestedModelSerializer):
    add_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    user = UsersSerializer()
    coord = CoordsSerializer()
    level = LevelSerializer()
    images = ImagesSerializer(many=True, required=False)
    status = serializers.CharField(read_only=True)

    def validate(self, validate_data):  # данный метод проверяет валидность данных от пользователся
        user_val_data = validate_data['user']
        user_original = self.instance.user
        error_messages = []

        # если данные внесены и объект взят в работу, то пользователь увидит предупреждение
        if self.instance and self.instance.status != 'new':
            error_messages.append({
                "message": "Данный перевал принят в работу, информацию о нем уже нельзя поменять",
                "state": "0"
            })

        if any(user_val_data[field] != getattr(user_original, field) for field in
               ('fam', 'name', 'otc', 'email', 'phone')):
            error_messages.append({
                "message": "Информацию о пользователе нельзя изменять.",
                "state": "0"
            })

        if error_messages:
            raise ValidationError(error_messages)

        validate_data['message'] = "Данные успешно изменены."
        validate_data['state'] = "1"

        return validate_data

    class Meta:
        model = Pereval
        fields = ['beauty_title',
                  'title',
                  'other_titles',
                  'connect',
                  'status',
                  'add_time',
                  'level',
                  'user',
                  'coord',
                  'images'
                  ]
