FROM python:3.10-slim

RUN mkdir /app

COPY . ./app

WORKDIR /app/server_simple_gram/backend/bot_django_project

RUN pip install --upgrade pip && pip install -r ../../requirements.txt --no-cache-dir

CMD ["gunicorn", "bot_constructor.wsgi:application", "--bind", "0:8000"]