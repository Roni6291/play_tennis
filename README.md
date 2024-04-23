# Play Tennis API

API for ML prediction endpoint.

## How to use ?

### using Docker

```sh
$ docker build --no-cache -t tennis_img:latest .
```

You can also pull from docker.io

```sh
$ docker image pull roniabraham06/tennis_img:latest
```

Run as container

```sh
$ docker run --name tennis -d -p 8000:8000 tennis_img:latest
```

### Using CLI

The package is available as a cli tool for inference as well. Currently only the inference functionalities are exposed. This can be extended for EDA, feature selection & scaling, feature engineering, hyperparamter tuning and training as well.

```sh
$ poetry run roger infer --help
```

![infer commands](./images/roger_infer_cli.png?raw=true "Inference Sub Commands")

### Using Poetry

#### Using ASGI uvicorn

```sh
$ poetry run asgi
```

#### Using WSGI gunicorn and uvicorn worker

`This will not work with windows OS`

```sh
$ poetry run wasgi
```