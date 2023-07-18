# GB_Python_Patterns
Архитектура и шаблоны проектирования на Python (разработка простейшего веб-фреймворка)

##Запуск
uwsgi --http :8080 --wsgi-file run.py


poetry export --without-hashes --format=requirements.txt > requirements.txt