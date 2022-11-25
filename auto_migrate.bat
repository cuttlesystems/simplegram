 @echo on
 
venv\Scripts\python.exe backend\bot_django_project\manage.py makemigrations
venv\Scripts\python.exe backend\bot_django_project\manage.py migrate
 
 pause



