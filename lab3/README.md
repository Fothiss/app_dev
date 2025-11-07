# Запуск приложения

## Вариант 1 (через VS Code) - самый простой:
1. Открыть папку `lab3` в VS Code
2. Открыть файл `main.py`
3. Нажать **Ctrl+F5**
4. Открыть http://localhost:8000/schema/swagger в браузере
5. Протестировать API через Swagger UI

## Вариант 2 (через командную строку):
1. Открыть командную строку в папке `lab3`
2. Выполнить: `python main.py`
3. Открыть http://localhost:8000 в браузере

## Команды для командной строки
### Вывод пользователей
```cmd
curl "http://localhost:8000/users"
```
### Добавление пользователя
```cmd
curl -X POST "http://localhost:8000/users" -H "Content-Type: application/json" -d "{\"username\":\"newuser\",\"email\":\"newuser@university.ru\"}"
```
### Вывод пользователя по ID
```cmd
curl "http://localhost:8000/users/6d2a5426-7ff0-4c0a-b47d-6eb2adbec788"
```

### Изменение информации о пользователе
```cmd
curl -X PUT "http://localhost:8000/users/30c12516-f982-4343-9806-5a62eb6b30aa" -H "Content-Type: application/json" -d "{\"email\":\"updated@university.ru\"}"
```

### Удаление информации о пользователе
```cmd
curl -X DELETE "http://localhost:8000/users/6d2a5426-7ff0-4c0a-b47d-6eb2adbec788"
```
### Получение информации по фильтру
```cmd
curl "http://localhost:8000/users?username=kozlov"
```
