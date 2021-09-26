FROM python:3.9-slim

ARG MODEL_NAME
ENV MODEL_NAME=${MODEL_NAME}

RUN mkdir -p \
    /usr/src/app/ \
    /usr/src/app/service

WORKDIR /usr/src/app/

COPY service/ service/
COPY urlclassifier/ urlclassifier/
COPY model/${MODEL_NAME} model.pkl
COPY [ "setup.py", \
       "logging.conf", \
       "requirements.txt", \
       "./" ]

RUN pip install --no-cache-dir \
    -r requirements.txt \
    -r service/service_requirements.txt \
    -e .

ENTRYPOINT [ "gunicorn", \
             "--bind=0.0.0.0:5000", \
             "--log-level=INFO", \
             "--access-logfile='-'", \
             "service.service:app" ]
