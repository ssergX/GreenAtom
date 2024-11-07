Этот проект представляет собой API для управления хранением отходов. 
Устанока зависимостей:
pip install -r requirements.txt
Запуск через docker:
docker-compose up --build
Наполнение базы данных тестовыми данными:
python manage.py populate_database
Тестирование контролера
python manage.py test storage.tests.test_views  
Тестирование моделей
python manage.py test storage.tests.test_models

