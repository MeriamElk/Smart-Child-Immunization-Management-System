from flask import Blueprint, request, jsonify
from flask_login import current_user
from controllers.enfant_controller import ajouter_enfant, lister_enfants, get_enfant, modifier_enfant, supprimer_enfant
from datetime import date

enfant_bp = Blueprint("enfant", __name__)

def calculer_age(date_naissance):
    today = date.today()
    return today.year - date_naissance.year - ((today.month, today.day) < (date_naissance.month, date_naissance.day))

@enfant_bp.route("/ajouter", methods=["POST"])
def route_ajouter_enfant():
    data = request.json
    enfant = ajouter_enfant(
        prenom=data.get("prenom"),
        nom=data.get("nom"),
        sexe=data.get("sexe"),
        date_naissance=data.get("date_naissance"),
        historique=data.get("historique"),
        utilisateur=current_user
    )
    if enfant:
        return jsonify({"message": "Enfant ajouté", "id": enfant.id_enfant})
    return jsonify({"error": "Ajout échoué"}), 400

@enfant_bp.route("/lister", methods=["GET"])
def route_lister_enfants():
    enfants = lister_enfants(utilisateur=current_user)
    return jsonify([
        {
            "id": e.id_enfant,
            "prenom": e.prenom,
            "nom": e.nom,
            "sexe": e.sexe,
            "age": calculer_age(e.date_naissance) if e.date_naissance else None,
            "statut_vaccinal": getattr(e, 'statut_vaccinal', None)
        } for e in enfants
    ])

@enfant_bp.route("/modifier/<int:id_enfant>", methods=["PUT"])
def route_modifier_enfant(id_enfant):
    data = request.json
    enfant = modifier_enfant(id_enfant, utilisateur=current_user, **data)
    if enfant:
        return jsonify({"message": "Enfant modifié", "id": enfant.id_enfant})
    return jsonify({"error": "Modification échouée"}), 400

@enfant_bp.route("/supprimer/<int:id_enfant>", methods=["DELETE"])
def route_supprimer_enfant(id_enfant):
    enfant = supprimer_enfant(id_enfant, utilisateur=current_user)
    if enfant:
        return jsonify({"message": "Enfant supprimé"})
    return jsonify({"error": "Suppression échouée"}), 404
