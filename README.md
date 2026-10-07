<<<<<<< HEAD
# Mini-Projet Docker : Site Web Vitrine & Tracking d'Interactions 
# -----------------------------------------------------------------------------------------------------------
# --------------------- Par Abimael Mahoungou, MS Expert Big Data Engineer ----------------------------------

Application web dynamique développée avec Flask et PostgreSQL, entièrement conteneurisée avec Docker et Docker Compose. Elle permet d'afficher une interface client et d'enregistrer en arrière-plan toutes les interactions des visiteurs en temps réel dans PostgreSQL.

## Architecture du projet

- **`app`** : Application Python Flask (Site vitrine + API de tracking).
- **`db`** : Base de données relationnelle PostgreSQL.
- **`adminer`** : Interface graphique de gestion pour visualiser les données stockées.

## Configuration requise

- [Docker Desktop](https://www.docker.com/)
- Git
   
## Accès aux services
# -----------------------------
Site vitrine intégrant le suivi dynamique des visites et des clics : http://localhost:5000

Interface Adminer (BDD) : http://localhost:8080

Système : PostgreSQL

Serveur : db

Utilisateur : user

Mot de passe : password

Base de données : taskdb

# Structure de la base de données
## Les interactions sont enregistrées dans la table interactions avec la structure suivante :

id : Identifiant unique.

page_url : Page consultée.

action_type : Type d'interaction (page_view, clic_bouton_interet, clic_bouton_contact).

user_agent : Navigateur du client.

ip_address : Adresse IP de l'utilisateur.

created_at : Horodatage exact de l'événement.

## Variables d'environnement
# ----------------------------------

Les variables de connexion à la base de données sont définies dans compose.yaml :

POSTGRES_DB=taskdb

POSTGRES_USER=user

POSTGRES_PASSWORD=password

DB_HOST=db

## Lancement rapide
# ----------------------------------

Cloner le projet :
   git clone https://github.com/Lanaza/Docker-project/
   cd Projet-docker

## Commandes utiles
# ----------------------------------

Voir les logs de l'application : docker compose logs -f app

Stopper les conteneurs : docker compose down

Stopper et supprimer les volumes : docker compose down -v
=======
# Docker-project
L'application est une interface web vitrine développée en Python avec le framework Flask, connectée à une base de données relationnelle PostgreSQL.  Elle permet de présenter un site client dynamique tout en enregistrant en temps réel toutes les interactions des visiteurs directement dans PostgreSQL.  
>>>>>>> 8c45e2c21b0e160a951d8de596a42beda158250a
