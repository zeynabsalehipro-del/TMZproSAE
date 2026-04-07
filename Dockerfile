# Utiliser l'image officielle Python
FROM python:3.12-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /code

# Copier le fichier des dépendances
COPY ./requirements.txt /code/requirements.txt

# Installer les dépendances
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copier le dossier 'app' dans le conteneur
COPY ./app /code/app

# Commande pour lancer l'application avec Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
