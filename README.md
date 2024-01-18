Проект Pereval_mod

1. Описание
Федерации Спортивного Туризма России (ФСТР) ведёт базу горных перевалов, которая пополняется туристами.

После преодоления очередного перевала, турист заполняет отчёт в формате PDF и отправляет его на электронную почту федерации. Экспертная группа ФСТР получает эту информацию, верифицирует, а затем вносит её в базу, которая ведётся в Google-таблице. Весь процесс очень неудобный и долгий и занимает в среднем от 3 до 6 месяцев.

ФСТР заказала разработать мобильное приложение для Android и IOS, которое упростило бы туристам задачу по отправке данных о перевале и сократило время обработки запроса до трёх дней.

Пользоваться мобильным приложением будут туристы. В горах они будут вносить данные о перевале в приложение и отправлять их в ФСТР, как только появится доступ в Интернет.

Модератор из федерации будет верифицировать и вносить в базу данных информацию, полученную от пользователей, а те в свою очередь смогут увидеть в мобильном приложении статус модерации и просматривать базу с объектами, внесёнными другими.

Требовалось разработать REST API, которое будет обслуживать мобильное приложение.
Для пользователя в мобильном приложении доступны следующие действия:
Внесение информации о новом объекте (перевале) в карточку объекта.
Редактирование в приложении неотправленных на сервер ФСТР данных об объектах, на перевале не всегда работает Интернет.
Заполнение ФИО и контактных данных (телефон и электронная почта) с последующим их автозаполнением при внесении данных о новых объектах.
Отправка данных на сервер ФСТР.
Получение уведомления о статусе отправки (успешно/неуспешно).
Согласие пользователя с политикой обработки персональных данных в случае нажатия на кнопку «Отправить» при отправке данных на сервер.
Пользователь с помощью мобильного приложения будет передавать в ФСТР следующие данные о перевале:
данные о пользователе: ФИО, телефон и email;
название перевала и его описание;
координаты перевала, его высота и сложность восхождение в разное время года;
несколько фотографий перевала.

2. Методы используемые в Rest API
После ввода данных турист нажимает кнопку «Отправить» в мобильном приложении. Мобильное приложение вызовет метод submitData REST API.

Метод submitData принимает JSON в теле запроса с информацией о перевале. Ниже находится пример такого JSON-а:

{
    "beauty_title": "	Белухинсний перевал",
    "title": "Белухинсний перевал (через вершину В. Белуха)",
    "other_titles": "Белуха",
    "connect": "", // что соединяет, текстовое поле
    "level": {
        "summer": "3B",
        "autumn": "3B",
        "winter": "3B",
        "spring": "3B"
    },
    "user": {
        "fam": "Грозный",
        "name": "Иван",
        "otc": "Васильевич",
        "email": "cometome@son.ru",
        "phone": "81234567890"
    },
    "coord": {
        "latitude": "49°48’8"N",
        "longitude": "86°35’25"E",
        "height": 4506
    },
    "images": [{"title": "Восхождение на Белуху через перевал Делоне", "image": "<изображение1>"},
    {"title": "Взгляд новичка или Белуха в марте", "image": "<изображение2>"}]
}
Результат метода: JSON

status — код HTTP, целое число:
500 — ошибка при выполнении операции;
400 — Bad Request (при нехватке полей);
200 — успех.
message — строка:
Причина ошибки (если она была);
Отправлено успешно;
Если отправка успешна, дополнительно возвращается id вставленной записи.
id — идентификатор, который был присвоен объекту при добавлении в базу данных.
Примеры:

{ "status": 500, "message": "Ошибка подключения к базе данных","id": null}
{ "status": 200, "message": null, "id": 42 }

После добавления в БД информации о новом перевале, со временем производится модерация нового объекта и изменяется его поле status.

Допустимые значения поля status:

new;
pending — если модератор взял в работу;
accepted — модерация прошла успешно;
rejected — модерация прошла, информация не принята.
Получение информации по одной записи:

Метод GET /submitData/<id>
Редактирование информации по одной записи:

Метод PATCH /submitData/<id>
Редактировать можно все поля, кроме тех, что содержат в себе ФИО, адрес почты и номер телефона. Метод принимает тот же самый json, который принимал метод POST submitData.

В качестве результата возвращается два значения:

state:
1 — если успешно удалось отредактировать запись в базе данных.
0 — в противном случае.
message - результат обновления.

Получение данных обо всех объектах, которые пользователь с почтой отправил на сервер

Метод GET /submitData/?user__email=<email>
Есть возможность фильтровать перевалы по нескольким полям, в том числе по e-mail.