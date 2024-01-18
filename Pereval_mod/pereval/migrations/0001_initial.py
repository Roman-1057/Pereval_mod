# Generated by Django 4.2.6 on 2024-01-09 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(max_length=25, verbose_name='Широта')),
                ('longitude', models.FloatField(max_length=25, verbose_name='Долгота')),
                ('height', models.IntegerField(verbose_name='Высота')),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summer', models.CharField(choices=[('1B', '1Б'), ('2A', '2А'), ('2B', '2Б'), ('3A', '3А'), ('3B', '3Б'), ('4A', '4А'), ('4B', '4Б'), ('5A', '5А'), ('5B', '5Б'), ('6A', '6А'), ('6B', '6Б')], max_length=2, verbose_name='Лето')),
                ('autumn', models.CharField(choices=[('1B', '1Б'), ('2A', '2А'), ('2B', '2Б'), ('3A', '3А'), ('3B', '3Б'), ('4A', '4А'), ('4B', '4Б'), ('5A', '5А'), ('5B', '5Б'), ('6A', '6А'), ('6B', '6Б')], max_length=2, verbose_name='Осень')),
                ('winter', models.CharField(choices=[('1B', '1Б'), ('2A', '2А'), ('2B', '2Б'), ('3A', '3А'), ('3B', '3Б'), ('4A', '4А'), ('4B', '4Б'), ('5A', '5А'), ('5B', '5Б'), ('6A', '6А'), ('6B', '6Б')], max_length=2, verbose_name='Зима')),
                ('spring', models.CharField(choices=[('1B', '1Б'), ('2A', '2А'), ('2B', '2Б'), ('3A', '3А'), ('3B', '3Б'), ('4A', '4А'), ('4B', '4Б'), ('5A', '5А'), ('5B', '5Б'), ('6A', '6А'), ('6B', '6Б')], max_length=2, verbose_name='Весна')),
            ],
        ),
        migrations.CreateModel(
            name='SprActivitiesTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('1', 'Пешком'), ('2', 'Лыжи'), ('3', 'Катамаран'), ('4', 'Байдарка'), ('5', 'Плот'), ('6', 'Сплав'), ('7', 'Велосипед'), ('8', 'Автомобиль'), ('9', 'Мотоцикл'), ('10', 'Парус'), ('11', 'Верхом')], max_length=25, verbose_name='Способ передвижения')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.IntegerField(verbose_name='Номер телефона')),
                ('fam', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('otc', models.CharField(max_length=100, verbose_name='Отчество')),
            ],
        ),
        migrations.CreateModel(
            name='Pereval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beauty_title', models.CharField(max_length=200, verbose_name='Топоним')),
                ('title', models.CharField(max_length=200, verbose_name='Название перевала')),
                ('other_titles', models.CharField(max_length=200)),
                ('connect', models.CharField(max_length=200)),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('status', models.CharField(choices=[('new', 'Создано'), ('pending', 'В работе'), ('accepted', 'Успешно'), ('rejected', 'Отклонено')], default='new', max_length=10, verbose_name='Статус заявки')),
                ('coord', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pereval.coords')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pereval.level')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pereval.users')),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название изображения')),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата добавления')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images', verbose_name='Изображение')),
                ('pereval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='pereval.pereval')),
            ],
        ),
    ]
