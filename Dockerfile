# Image de base officielle avec un tag figé
FROM python:3.11-slim

# Repertoire de travail dans le conteneur
WORKDIR /app

# Installation des dépendances en premier pour optimiser le cache Docker
COPY app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie du reste du code source
COPY app/ .

# Commande de démarrage sous forme exec (tableau JSON)
CMD ["python", "main.py"]