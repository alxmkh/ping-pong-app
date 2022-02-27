FROM python:3.10.1-alpine

RUN mkdir -p /ping-pong-app

RUN /usr/local/bin/python -m pip install --upgrade pip && pip install pipenv

ENV PROJECT_DIR /ping-pong-app

WORKDIR ${PROJECT_DIR}

COPY Pipfile* ${PROJECT_DIR}/

RUN pipenv install --system --deploy

COPY . ${PROJECT_DIR}

RUN cd ${PROJECT_DIR}

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "4001"]
