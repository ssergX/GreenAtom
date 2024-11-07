<h1 align="center"> Этот проект представляет собой API для управления хранением отходов. </h1>
<ol> 
Устанока зависимостей:
<li>  pip install -r requirements.txt </li>
<li> Запуск через docker:
docker-compose up --build  </li>
<li> Наполнение базы данных тестовыми данными:
python manage.py populate_database  </li>
<li> Тестирование контролера
python manage.py test storage.tests.test_views    </li>
<li> Тестирование моделей
python manage.py test storage.tests.test_models  </li>
 </ol>
