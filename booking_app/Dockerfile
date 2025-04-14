FROM python:3.12-bookworm

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --only main


COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:main_app", "--host", "0.0.0.0", "--port", "8000", "--reload"]