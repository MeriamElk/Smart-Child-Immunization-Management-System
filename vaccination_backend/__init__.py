from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Initialisation de SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()

def init_app(app):
    # Configuration de la base de données
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:root@localhost/vaccination_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialisation des extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Création des tables
    with app.app_context():
        db.create_all() 