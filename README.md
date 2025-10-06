VacciTrack – Système de Suivi des Vaccinations Infantiles
VacciTrack est une application web conçue pour faciliter le suivi des vaccinations des enfants. Elle permet aux parents, médecins et administrateurs de gérer les dossiers vaccinaux, générer des alertes de rappel, et analyser la couverture vaccinale.

Prérequis techniques
Python 3.9+

MySQL Server (v8.x recommandé)

MongoDB (local, ex: localhost:27017)

Pip + venv pour l’environnement virtuel

Installation & Configuration

Créer un environnement virtuel et l’activer

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

Installer les dépendances

bash
Copier le code
pip install -r requirements.txt
Configurer MySQL

Lancer le script SQL :

bash
Copier le code
mysql -u root -p < data/create_mysql_schema.sql
Configurer MongoDB

Démarrer le serveur MongoDB (sur localhost:27017)

Exécuter :


python data/initialize_mongodb.py
▶
Exécution de l'application
Lancer le serveur Flask

python app.py

Accéder à l’interface

Ouvrir : http://127.0.0.1:5000/ dans un navigateur

Rôles utilisateurs
Parent : Voir les enfants, recevoir des alertes

Médecin : Gérer les vaccinations et analyses

Admin : Gérer tous les utilisateurs

Technologies utilisées
Flask (backend)

MySQL + SQLAlchemy (relationnel)

MongoDB (NoSQL - alertes & logs)

Jinja2, HTML/CSS, JavaScript (frontend)

Bcrypt, JWT (sécurité)

Données de test incluses
Comptes précréés (emails + mots de passe hashés)

Données d’enfants, vaccinations, vaccins, alertes
