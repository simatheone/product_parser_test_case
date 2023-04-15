FROM python:3.10-alpine as requirements-stage

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /tmp

RUN pip3.10 install poetry

WORKDIR .

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10-alpine

WORKDIR /product_parser

COPY --from=requirements-stage /tmp/requirements.txt /product_parser/requirements.txt

RUN pip3.10 install --upgrade pip && \
    pip3.10 install -r /product_parser/requirements.txt --no-cache-dir

WORKDIR .

COPY . /product_parser

WORKDIR /product_parser

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
