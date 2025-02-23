FROM docker.io/library/python:3.12-slim-bookworm AS builder

WORKDIR /install
COPY requirements.txt .

RUN python3 -m pip install --no-cache-dir --upgrade cython pip && \
    python3 -m pip install --no-cache-dir --target=/install torch==2.5.1 && \
    python3 -m pip install --no-cache-dir --target=/install -r requirements.txt


FROM python:3.12-slim-bookworm

RUN useradd -m myuser

ENV HTTP_PORT=8000
ENV HF_HOME=/app/cache
ENV PYTHONPATH=/app

COPY --from=builder /install /usr/local/lib/python3.12/site-packages
WORKDIR /app

COPY . .

RUN chown -R myuser:myuser /app
USER myuser

CMD ["python3", "instance/app.py", "--port", "$HTTP_PORT"]
