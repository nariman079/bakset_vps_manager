# ООО "БАКСЕТ" VPS Менеджер

Сервис для управления виртуальными серверами (VPS) с использованием современных технологий.

## Основные функции
- **Создание нового виртуального сервера**: Легко создавайте новые виртуальные серверы с заданными параметрами.
- **Получение детальной информации о сервере**: Получайте подробную информацию о сервере по его уникальному идентификатору (UID).
- **Вывод списка всех серверов**: Просматривайте список всех серверов с возможностью фильтрации по различным параметрам.
- **Изменение статуса сервера**: Управляйте состоянием сервера (например, запуск, блокировка, остановка).

## Технологии
- **Python**: Основной язык программирования для разработки сервиса.
- **Django Rest Framework**: Фреймворк для создания RESTful API.
- **SQLite3**: Легковесная база данных для хранения информации о серверах.
- **Docker Compose**: Инструмент для оркестрации контейнеров, используемый для виртуализации серверов в этом проекте.


## Что можно добавить ?
- Резервное копирование и восстановление данных
- Автоматическое масштабирование ресурсов
- Почасовая оплата серверов
- Мониторинг и аналитика
- Поддержка нескольких операционных систем
- Уведомления и оповещения

## Запуск проекта
### Важные замечания
Данный проект использует Docker для виртуализации серверов. Это позволяет быстро разворачивать и управлять виртуальными серверами в изолированных контейнерах. Однако важно понимать, что Docker не является полноценной заменой традиционных решений для виртуализации, таких как KVM, VMware или Hyper-V. Docker больше подходит для разработки, тестирования и изоляции приложений, но не для создания полноценных виртуальных серверов с высокой степенью изоляции и производительности.
### Требования
- **Docker** и **Docker Compose** должны быть установлены на вашей системе.
- **Python** версии 3.11 или выше.

### Установка и запуск

#### Для Windows

1. **Установите Docker Desktop**:
   - Скачайте и установите Docker Desktop с [официального сайта](https://www.docker.com/products/docker-desktop).
   - Убедитесь, что Docker Desktop запущен.

2. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/nariman079/bakset_vps_manager.git
   cd bakset_vps_manager
   ```
3. **Выполните команды**:
   ```bash
   make run
    ```
#### Для Ubuntu
1. **Установите Docker Engine**:
   - Скачайте и установите Docker Engine с [официального сайта](https://docs.docker.com/engine/install/).
   - Убедитесь, что Docker Engine запущен.

2. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/nariman079/bakset_vps_manager.git
   cd bakset_vps_manager
   ```
3. **Выполните команды**:
   ```bash
   make run
    ```

После выполнения всех иструкций у вас должен запуститься проект и вы можете перейти на страницу списка серверов http://localhost:8000/api/servers/

# Документация к API

## 1 - Добавление сервера
### `POST` /api/servers/
#### Headers
```json
{
    "Content-Type": "application/json",
}
```
#### Request Data
Описание полей:
- **hdd** (float): Физическая память для сервера. 
- **cpu** (int): Количество ядер для сервера
- **ram** (float): Оперативная память для сервера
- **ssh_key** (str): Установка вашего ssh ключа, чтобы можно было подключиться к серверу без пароля
- **server_password** : Установка вашего пароля для пользователя root
```json
{
    "hdd": 1, 
    "cpu": 1, 
    "ram": 1, 
    "ssh_key": "ssh key", 
    "server_password": "1234", 
}
```
#### Response
##### 201
```json
{
    "message": "Сервер создается и будет готов к работе через 60-90 секунд",
    "data": {
        "ip": "46.200.0.2",
        "shh_connection": "ssh root@46.200.0.2",
        "password": "gnyaR3OpOnQH",
        "server": {
            "uid": "22a483b2-c9fc-4040-b9fa-bdccca2b50b0",
        }
    }
}
```
## 2 - Изменение статуса сервера
### `PATCH` /api/servers/{uid}/change_status/
#### Headers
```json
{
    "Content-Type": "application/json",
}
```
#### Request Data
Доступные статусы:
- **started** : Запуск сервера
- **blocked** : Блокировка сервера, пользователи не смогут подключиться по ssh
- **unblocked** : Разблокировка сервера, пользователям вновь доступно подключение по ssh
- **stopped** : Полная остановка сервера
```json
{
    "status": "started" 
}
```
#### Response
##### 200
```json
{
    "message": "Статус сервера изменился на started"
}
```
## 3 - Получение списка серверов с возможностью фильтрации
### `GET` /api/servers/
#### Request query params
Поля для фильтрации:
- **status**
- **id**
- **hdd**
- **cpu**
- **ram**
#### Response
##### 200
```json
[
    {
        "id": 1,
        "uid": "9afd4061-b080-4955-8d9c-5767b724c63f",
        "public_ip": "98.103.0.2",
        "status": "started"
    }
]
```

## 4 - Получение детальной информации о сервере
### `GET` /api/servers/{uid}
#### Response
##### 200
```json
{
    "id": 1,
    "uid": "9afd4061-b080-4955-8d9c-5767b724c63f",
    "hdd": 1.0,
    "cpu": 1,
    "ram": 0.1,
    "password": "TFL3negFVAF5",
    "public_ip": "98.103.0.2",
    "server_os": "ubuntu:22.04",
    "status": "started"
}
```
