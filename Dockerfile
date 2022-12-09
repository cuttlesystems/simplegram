FROM python:3.10-slim

RUN mkdir /app

COPY ./ ./app

WORKDIR /app/backend/bot_django_project

RUN pip install --upgrade pip && pip3 install -r ../../requirements.txt --no-cache-dir && python manage.py migrate

CMD ["gunicorn", "bot_constructor.wsgi:application", "--bind", "0:8000"]