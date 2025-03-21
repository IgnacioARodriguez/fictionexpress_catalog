FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    libmariadb-dev \
    gcc \
    python3-dev \
    build-essential

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 4. Instalar dependencias
RUN pip install --upgrade pip \
    && pip install mysqlclient \
    && pip install --no-cache-dir -r requirements.txt


COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
