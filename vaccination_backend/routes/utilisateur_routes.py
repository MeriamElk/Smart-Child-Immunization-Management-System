from flask import Blueprint, request, jsonify
from flask_login import current_user
from controllers.utilisateur_controller import (
    ajouter_utilisateur,
    get_utilisateur,
    modifier_utilisateur,
    supprimer_utilisateur
)

utilisateur_bp = Blueprint("utilisateur", __name__)

@utilisateur_bp.route("/ajouter", methods=["POST"])
def route_ajouter_utilisateur():
    data = request.json
    user = ajouter_utilisateur(
        email=data.get("email"),
        role=data.get("role"),
        mot_de_passe=data.get("mot_de_passe"),
        utilisateur=current_user
    )
    if user:
        return jsonify({"message": "Utilisateur ajouté", "id": user.id_utilisateur})
    return jsonify({"error": "Échec de création"}), 400

@utilisateur_bp.route("/get", methods=["GET"])
def route_get_utilisateur():
    email = request.args.get("email")
    user = get_utilisateur(email, utilisateur=current_user)
    if user:
        return jsonify({"email": user.email, "role": user.role})
    return jsonify({"error": "Utilisateur introuvable"}), 404

@utilisateur_bp.route("/modifier/<int:id_utilisateur>", methods=["PUT"])
def route_modifier_utilisateur(id_utilisateur):
    data = request.json
    user = modifier_utilisateur(id_utilisateur, utilisateur=current_user, **data)
    if user:
        return jsonify({"message": "Utilisateur modifié", "id": user.id_utilisateur})
    return jsonify({"error": "Modification échouée"}), 400

@utilisateur_bp.route("/supprimer/<int:id_utilisateur>", methods=["DELETE"])
def route_supprimer_utilisateur(id_utilisateur):
    user = supprimer_utilisateur(id_utilisateur, utilisateur=current_user)
    if user:
        return jsonify({"message": "Utilisateur supprimé"})
    return jsonify({"error": "Suppression échouée"}), 404
