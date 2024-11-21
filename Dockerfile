FROM python:3.11-bullseye

WORKDIR /app

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml


COPY .env .

RUN  pip install --upgrade pip \
     && pip install poetry \
     && poetry config virtualenvs.create false \
     && poetry install --no-root --no-dev

COPY src ./src

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]