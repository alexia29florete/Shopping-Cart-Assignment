# Folosim imagine Python minimală
FROM python:3.12-alpine

# Setăm variabila de mediu pentru Flask
ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Instalăm dependințele necesare
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiem tot proiectul în container
COPY . .

# Expunem portul pe care rulează Flask
EXPOSE 5000

# Comanda de rulare
CMD ["flask", "run"]
