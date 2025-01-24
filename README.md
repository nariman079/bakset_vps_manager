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

## Запуск проекта

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
   make init
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
   make init
   make run
    ```

После выполнения всех  иструкций у вас должен запуститься проект и вы можете перейти на страницу списка серверов http://localhost:8000/api/servers/

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
```json
{
    "hdd": 1,
    "cpu": 1,
    "ram": 1,
    "ssh_key": "ssh key", // Необязательное поле
    "server_password": "1234", // Необязательное поле
}
```
#### Response
##### 201
```json
{
    "message": "Сервер создается и будет готов к работе через 60-90 секунд",
    "data": {
        "ip": "46.200.0.2",
        "web_terminal_url": "http://46.200.0.2:7681/",
        "shh_connection": "ssh root@46.200.0.2",
        "password": "gnyaR3OpOnQH",
        "server": {
            "image": "ubuntu:22.04",
            "name": "22a483b2-c9fc-4040-b9fa-bdccca2b50b0",
        }
    }
}
```
## 1 - Изменение статуса сервера
### `POST` /api/servers/{uid}/change_status/
#### Headers
```json
{
    "Content-Type": "application/json",
}
```
#### Request Data
```json
{
    "status": "started" // Варианты статуса (started, blocked, stopped)
}
```
#### Response
##### 201
```json
{
    "message": "Ваш сервер запускается и будет готов через 15-20 секунд"
}
```
или
```json
{
    "message": "Ваш сервер остановлен"
}
```
или
```json
{
    "message": "Ваш сервер заблокирован"
}
```
## 1 - Изменение статуса сервера
### `POST` /api/servers/{uid}/change_status/
#### Headers
```json
{
    "Content-Type": "application/json",
}
```
#### Request Data
```json
{
    "status": "started"
}
```
#### Response
##### 201
```json
{
    "message": "Ваш сервер запускается и будет готов через 15-20 секунд"
}
```
или
```json
{
    "message": "Ваш сервер остановлен"
}
```
или
```json
{
    "message": "Ваш сервер заблокирован"
}
```