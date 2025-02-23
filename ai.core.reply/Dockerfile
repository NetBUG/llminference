FROM python:3.12-slim-bookworm AS py312-torch-base

COPY requirements.txt .

RUN python3 -m pip install --no-cache-dir --upgrade cython pip && \
    python3 -m pip install --no-cache-dir torch==2.5.1 && \
    python3 -m pip install --no-cache-dir -r requirements.txt

ARG PORT=8000

WORKDIR /app

ENV HTTP_PORT=${PORT}
ENV HF_HOME=/app/cache
ENV PYTHONPATH=/app

EXPOSE ${HTTP_PORT}/tcp

COPY . .

CMD python3 instance/app.py --port ${HTTP_PORT}
