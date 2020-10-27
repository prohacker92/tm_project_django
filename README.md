## Система сбора СМС сообщений с телеметрией с электрических подстанций
Проект разработан в рамках дипломной работы для энергетической компании.

Система состоит из веб-приложения на Django 2.2.6 и модуля на python3.7 для работы с USB модемом для приема и отправки СМС.

Веб приложение состоит из:
- *my_app* (не удачное название). Отображение главной страницы на которой обновляется список принятых СМС сообщений.
- *archive*. Страница для получения выгрузки сообшений с выбранных обьектов за период.
- *signal_PS*. Страница со списком доступных для пользователя подстанций для просмотра состояния сигналов собираемых с выбранной подстанции.
- *support_contacts*. Контактная информация.
Пользователи и подстанции разбиты по группам, каждый пользователь получает сообщения только с тех подстанций в группах которых состоит.

Для написания sms_modules использовалась библиотека python-gsmmodem-new [github](https://github.com/babca/python-gsmmodem).
Данный модуль сохраняет принимаемые СМС сообщения в БД используя ORM систему Django и позволяет отправлять СМС запросы на GSM контроллеры установленные на подстанциях. Также модуль отвечает за дополнительное оповещение пользователей по СМС о не просмотренных сообщениях на главной странице за установленное время.
