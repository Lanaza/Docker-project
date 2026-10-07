---
Title: "RAPPORT TECHNIQUE - MINI PROJET DOCKER"
subtitle: "Conteneurisation d'un site vitrine avec tracking d'interactions et PostgreSQL"
Author: "Abimael MAHOUNGOU, MS Expert Big Data Engineer"
Date: "07-10-2026"
Output: Markdown document
---

## 1. Description générale de l'application

L'application est une interface web vitrine développée en Python avec le framework **Flask**, connectée à une base de données relationnelle **PostgreSQL**.

Elle permet de présenter un site client dynamique tout en enregistrant en temps réel toutes les interactions des visiteurs (consultations de pages, clics sur les boutons de contact ou d'intérêt) directement dans PostgreSQL.

- **Site Web Client (`http://localhost:5000`)** : Interface vitrine intuitive permettant aux utilisateurs de naviguer et d'interagir avec la page.
- **API de tracking (`POST /api/track`)** : Endpoint REST interne recevant les événements et assurant leur persistance en BDD.
- **Adminer (`http://localhost:8080`)** : Interface graphique de gestion et de visualisation permettant d'analyser la table `interactions` stockée dans PostgreSQL.

---

## 2. Réponses aux questions techniques du sujet

**- Question 1 : Choix de l'image de base pour le service Flask**

**Image sélectionnée** : `python:3.11-slim`

*Justification* : 
L'image `slim` offre un excellent équilibre entre légèreté et compatibilité logicielle. Basée sur une distribution Debian allégée, elle permet d'installer rapidement des paquets Python précompilés (*wheels*) et les dépendances nécessaires comme `psycopg2` tout en maintenant une taille d'image réduite par rapport à l'image Python standard.

**- Question 2 : Optimisation du cache de build Docker**

Dans le fichier `Dockerfile`, les instructions ont été structurées dans cet ordre précis :


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .

*Explication* :

Docker met en cache chaque couche du build. Les dépendances Python (requirements.txt) évoluent rarement, tandis que le code source (main.py) change fréquemment. En séparant l'installation des dépendances avant la copie du code applicatif, Docker réutilise la couche de cache lors des builds ultérieurs si le fichier requirements.txt n'a pas été modifié.

**- Question 3 : Analyse de la taille de l'image finale**

Taille de l'image du projet docker : 54,5 Mo.

Pistes d'optimisation futures :

Build multi-étapes (Multi-stage build) : Compiler les dépendances dans une étape temporaire et ne copier que l'environnement d'exécution dans l'image finale.

Nettoyage du cache pip : Utiliser le paramètre --no-cache-dir lors de l'exécution de pip install.

**- Question 4 : Stratégie de persistance des données**

La persistance des données PostgreSQL est assurée par un volume nommé Docker configuré dans le fichier compose.yaml :

YAML
volumes:
  postgres_data:
Ce volume est monté sur le dossier /var/lib/postgresql/data du conteneur db.

*Comportement avec docker compose down* : Les conteneurs sont arrêtés et supprimés, mais le volume postgres_data est conservé sur la machine hôte. 
Au redémarrage (docker compose up -d), l'intégralité des données et de l'historique est restaurée.

*Comportement avec docker compose down -v* : Les conteneurs ET les volumes sont détruits. La base de données est réinitialisée à zéro.

**- Question 5 : Difficultés rencontrées et solutions apportées**
 ### Conflit d'exposition du port hôte (5000) :

    *Problème : Le port 5000 était déjà réservé sur la machine hôte.

    *Solution : Libération du port via PowerShell (Stop-Process) ou configuration explicite du mapping 5000:5000 dans compose.yaml.

 ### Délai d'initialisation de PostgreSQL :

    *Problème : Au premier démarrage, PostgreSQL prend quelques secondes à s'initialiser. Flask tentait de s'y connecter immédiatement, provoquant une erreur de connexion.

    *Solution : Mise en place d'un mécanisme de réessai automatique (retry logic) dans main.py pour attendre que la BDD soit prête.

 ### Séparation de l'expérience vitrine et de l'administration :

    *Problème : Les interactions s'affichaient directement sur le site client.

    *Solution : Conservation d'une interface utilisateur épurée et réservation de la consultation de l'historique d'interactions à l'interface d'administration Adminer
