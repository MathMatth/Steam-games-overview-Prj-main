# Utilisez une image Python officielle comme image de base
FROM python:3.10

# Définissez le répertoire de travail dans le conteneur
WORKDIR /bloc_4_DL

# Copiez le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Copiez l'ensemble du contenu de votre application dans le conteneur
COPY . .

# Copiez le contenu du répertoire "uploads" dans le conteneur
COPY ./uploads /uploads

# Copiez le contenu du répertoire "model" dans le conteneur
COPY ./model /model

# Copiez le contenu du répertoire "Who_s_that_Champ" dans le conteneur
COPY ./Who_s_that_Champ /Who_s_that_Champ

# Installez les dépendances à partir du fichier requirements.txt
RUN pip install -r requirements.txt

# Donner les droits d'écriture au répertoire "uploads"
RUN chmod -R 777 /uploads

# Exposez le port que votre application Flask utilise (par défaut, c'est le port 5000)
EXPOSE 5000

# Commande pour exécuter votre application Flask
CMD ["python", "app.py"]
