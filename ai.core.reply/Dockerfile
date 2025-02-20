FROM python:3.12-slim-bookworm AS py312-torch-base
# FROM gcr.io/distroless/python3-debian12

COPY requirements.txt .

RUN python3 -m pip install --upgrade cython pip && \
    python3 -m pip install torch==2.5.1 && \
    python3 -m pip install -r requirements.txt


FROM py312-torch-base

ARG PORT=8000

WORKDIR /app

COPY . .

ENV HTTP_PORT=${PORT}
ENV HF_HOME=/app/cache
ENV PYTHONPATH=/app

EXPOSE ${HTTP_PORT}/tcp

CMD python3 instance/app.py --port ${HTTP_PORT}
