from django.db import models


class Users(models.Model):  # модель данных пользователя
    email = models.EmailField(max_length=100)
    phone = models.IntegerField(verbose_name='Номер телефона')
    fam = models.CharField(max_length=100, verbose_name='Фамилия')
    name = models.CharField(max_length=100, verbose_name='Имя')
    otc = models.CharField(max_length=100, verbose_name='Отчество')

    def __str__(self):
        return f'email: {self.email}, phone: {self.phone}, fam: {self.fam}, name: {self.name}, otc: {self.otc}'


class Coords(models.Model):  # модель данных координат
    latitude = models.FloatField(max_length=25, verbose_name='Широта')
    longitude = models.FloatField(max_length=25, verbose_name='Долгота')
    height = models.IntegerField(verbose_name='Высота')

    def str(self):
        return f'Широта: {self.latitude}, долгота: {self.longitude}, высота: {self.height}'


class Level(models.Model):   # уровни сложности в зависимости от сезона
    LEVEL = [
        ('1B', '1Б'),
        ('2A', '2А'),
        ('2B', '2Б'),
        ('3A', '3А'),
        ('3B', '3Б'),
        ('4A', '4А'),
        ('4B', '4Б'),
        ('5A', '5А'),
        ('5B', '5Б'),
        ('6A', '6А'),
        ('6B', '6Б')
    ]

    summer = models.CharField(max_length=2, choices=LEVEL, verbose_name='Лето')
    autumn = models.CharField(max_length=2, choices=LEVEL, verbose_name='Осень')
    winter = models.CharField(max_length=2, choices=LEVEL, verbose_name='Зима')
    spring = models.CharField(max_length=2, choices=LEVEL, verbose_name='Весна')

    def str(self):
        return f'Уровни сложности перевала: лето: {self.summer}, осень: {self.autumn}, зима: {self.winter}, ' \
               f'весна: {self.spring}.'


class Pereval(models.Model):  # главная модель - перевал

    STATUS = [
        ('new', 'Создано'),
        ('pending', 'В работе'),
        ('accepted', 'Успешно'),
        ('rejected', 'Отклонено')
    ]

    beauty_title = models.CharField(max_length=200, verbose_name='Топоним')
    title = models.CharField(max_length=200, verbose_name='Название перевала')
    other_titles = models.CharField(max_length=200, verbose_name='Другие названия')
    connect = models.CharField(max_length=200, verbose_name='Соединение')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    status = models.CharField(max_length=10, choices=STATUS, default='new', verbose_name="Статус заявки")

    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    coord = models.OneToOneField(Coords, on_delete=models.CASCADE)

    def str(self):
        return f'Перевал № {self.pk}: {self.beauty_title},{self.title} имеет статус {self.status}.'


class Images(models.Model):  # модель для обработки изображений перевалов
    title = models.CharField(max_length=200, verbose_name='Название изображения')
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Дата добавления')
    image = models.ImageField(upload_to='images', verbose_name='Изображение', blank=True, null=True)
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='images')


class SprActivitiesTypes(models.Model):  # модель для обработки способа передвижения в походе

    TYPE = [
        ('1', 'Пешком'),
        ('2', 'Лыжи'),
        ('3', 'Катамаран'),
        ('4', 'Байдарка'),
        ('5', 'Плот'),
        ('6', 'Сплав'),
        ('7', 'Велосипед'),
        ('8', 'Автомобиль'),
        ('9', 'Мотоцикл'),
        ('10', 'Парус'),
        ('11', 'Верхом'),
    ]

    title = models.CharField(max_length=25, choices=TYPE, verbose_name='Способ передвижения')