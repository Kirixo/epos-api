FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN pip install mypy

COPY mypy.ini .
COPY ./app ./app
COPY ./etc ./etc
COPY ./tests ./tests
#COPY ./alembic.ini ./alembic.ini
#COPY ./pytest.ini ./pytest.ini

EXPOSE 8000

RUN mypy .

CMD ["sh", "-c", "uvicorn app.main:app --port ${API_PORT} --host ${API_HOST}"]
