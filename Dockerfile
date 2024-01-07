FROM python:3.12

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY solaredge_influxdb ./

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD ["python", "-m", "solaredge_influxdb"]