FROM python:3.10

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-root

COPY . /app

CMD ["scrapy", "crawl", "fix_price"]