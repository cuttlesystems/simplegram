FROM python:3.10-slim

RUN mkdir /app

COPY ./ ./app

RUN pip install --upgrade pip && pip3 install -r ./app/requirements.txt --no-cache-dir

WORKDIR /app/backend/bot_django_project

CMD ["gunicorn", "bot_constructor.wsgi:application", "--bind", "0:8000"]