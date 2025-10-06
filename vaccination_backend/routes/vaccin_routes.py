from flask import Blueprint, request, jsonify
from flask_login import current_user
from controllers.vaccin_controller import ajouter_vaccin, lister_vaccins, modifier_vaccin, supprimer_vaccin

vaccin_bp = Blueprint("vaccin", __name__)

@vaccin_bp.route("/ajouter", methods=["POST"])
def route_ajouter_vaccin():
    data = request.json
    vaccin = ajouter_vaccin(
        nom=data.get("nom"),
        age=data.get("age"),
        doses=data.get("doses"),
        effets=data.get("effets"),
        type_vaccin=data.get("type_vaccin"),
        maladies=data.get("maladies"),
        utilisateur=current_user
    )
    if vaccin:
        return jsonify({"message": "Vaccin ajouté", "id": vaccin.vaccin_id})
    return jsonify({"error": "Ajout échoué"}), 400

@vaccin_bp.route("/lister", methods=["GET"])
def route_lister_vaccins():
    vaccins = lister_vaccins(utilisateur=current_user)
    return jsonify([
        {
            "id": v.vaccin_id,
            "nom": v.nom_vaccin,
            "age": v.age_recommande
        } for v in vaccins
    ])

@vaccin_bp.route("/modifier/<int:vaccin_id>", methods=["PUT"])
def route_modifier_vaccin(vaccin_id):
    data = request.json
    vaccin = modifier_vaccin(vaccin_id, utilisateur=current_user, **data)
    if vaccin:
        return jsonify({"message": "Vaccin modifié", "id": vaccin.vaccin_id})
    return jsonify({"error": "Modification échouée"}), 400

@vaccin_bp.route("/supprimer/<int:vaccin_id>", methods=["DELETE"])
def route_supprimer_vaccin(vaccin_id):
    vaccin = supprimer_vaccin(vaccin_id, utilisateur=current_user)
    if vaccin:
        return jsonify({"message": "Vaccin supprimé"})
    return jsonify({"error": "Suppression échouée"}), 404
