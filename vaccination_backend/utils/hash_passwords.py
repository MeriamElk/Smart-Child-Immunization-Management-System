from flask import Flask
from werkzeug.security import generate_password_hash
from vaccination_backend import init_app, db
from vaccination_backend.models.utilisateur import Utilisateur

app = Flask(__name__)

init_app(app)

# Contexte Flask pour accéder à la base
with app.app_context():
    utilisateurs = Utilisateur.query.all()
    for user in utilisateurs:
        if not user.mot_de_passe.startswith("pbkdf2:sha256"):
            user.mot_de_passe = generate_password_hash(user.mot_de_passe)
            print(f"Hachage de : {user.email}")
    db.session.commit()
    print("Tous les mots de passe ont été hachés avec succès.")
