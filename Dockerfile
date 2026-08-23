FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias Python primero para aprovechar la cache de Docker
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Reflex:
# 3000 -> frontend
# 8000 -> backend
EXPOSE 3000 8000

CMD ["reflex", "run", "--env", "prod"]