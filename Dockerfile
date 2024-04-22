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

ENV PIP_ROOT_USER_ACTION=ignore

RUN mkdir -p /opt/tennis/models /opt/tennis/dist

WORKDIR /opt/tennis

COPY --from=requirements-stage /tmp/requirements.txt /tmp/app.py /opt/tennis/
COPY --from=requirements-stage /tmp/dist /opt/tennis/dist
COPY --from=requirements-stage /tmp/models /opt/tennis/models

RUN chmod +x /opt/tennis/* && \
    python3 -m pip install --upgrade pip && \
    pip install \
        --no-cache-dir \
        -r /opt/tennis/requirements.txt && \
    pip install /opt/tennis/dist/roger-0.1.0-py3-none-any.whl

EXPOSE 8000

CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:8000","-k", "uvicorn.workers.UvicornWorker", "app:app"]