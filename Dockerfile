# Utilisez une image de base Python, par exemple
FROM python:3.9

# Copiez les fichiers de l'application dans le conteneur
COPY . /app

# Définissez le répertoire de travail comme répertoire de l'application
WORKDIR /app

# Installez les dépendances de l'application
RUN pip install -r requirements.txt

# Exposez le port sur lequel votre application Panel s'exécute
EXPOSE 5006

# Définissez la commande pour lancer votre application Panel
CMD ["panel", "serve", "--address", "0.0.0.0", "--port", "5006", "hmi.py"]