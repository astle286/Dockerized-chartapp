FROM python:3.14.2-bookworm AS builder

RUN apt-get update && apt-get install -y build-essential libfreetype6-dev libpng-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


FROM python:3.14.2-slim-bookworm

RUN apt-get update && apt-get install -y libfreetype6 libpng-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /wheels /wheels

RUN pip install --no-cache-dir /wheels/* gunicorn

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000","app:app"]