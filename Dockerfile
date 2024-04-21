FROM python:3.10 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY . /tmp/

RUN poetry export \
        -f requirements.txt \
        --output requirements.txt \
        --without-hashes && \
    poetry build --format=wheel

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

RUN mkdir -p /opt/tennis

WORKDIR /opt/tennis

COPY --from=requirements-stage /tmp/requirements.txt /tmp/dist/ /tmp/app.py /tmp/models/ ./

RUN chmod +x /opt/tennis/* && \
    pip install \
        --no-cache-dir \
        -r /opt/requirements.txt && \
    pip install /opt/tennis/dist/*.whl

CMD ["gunicorn", "app:app" "--workers" "2" "--host", "0.0.0.0", "--port", "8000"]