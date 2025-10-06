from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user
from vaccination_backend.models.utilisateur import Utilisateur
import bcrypt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    mot_de_passe = data.get("mot_de_passe")

    if not email or not mot_de_passe:
        return jsonify({"error": "Email et mot de passe requis"}), 400

    utilisateur = Utilisateur.query.filter_by(email=email).first()

    if utilisateur and bcrypt.checkpw(mot_de_passe.encode(), utilisateur.mot_de_passe.encode()):
        login_user(utilisateur)
        return jsonify({
            "message": "Connexion réussie",
            "id": utilisateur.id_utilisateur,
            "role": utilisateur.role,
            "email": utilisateur.email
        })
    return jsonify({"error": "Identifiants invalides"}), 401

@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify({"message": "Déconnexion réussie"})
