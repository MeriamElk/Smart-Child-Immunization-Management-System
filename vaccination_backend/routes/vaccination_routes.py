from flask import Blueprint, request, jsonify
from flask_login import current_user
from controllers.vaccination_controller import enregistrer_vaccination, lister_vaccinations, modifier_vaccination, supprimer_vaccination

vaccination_bp = Blueprint("vaccination", __name__)

@vaccination_bp.route("/ajouter", methods=["POST"])
def route_enregistrer_vaccination():
    data = request.json
    vaccination = enregistrer_vaccination(
        id_enfant=data.get("id_enfant"),
        vaccin_id=data.get("vaccin_id"),
        dose=data.get("dose"),
        statut=data.get("statut"),
        utilisateur=current_user
    )
    if vaccination:
        return jsonify({"message": "Vaccination enregistrée", "id": vaccination.id_vaccination})
    return jsonify({"error": "Échec"}), 400

@vaccination_bp.route("/lister", methods=["GET"])
def route_lister_vaccinations():
    vaccinations = lister_vaccinations(utilisateur=current_user)
    return jsonify([
        {
            "id": v.id_vaccination,
            "enfant_id": v.id_enfant,
            "vaccin_id": v.vaccin_id,
            "dose": v.dose,
            "statut": v.statut_vaccination
        } for v in vaccinations
    ])

@vaccination_bp.route("/modifier/<int:id_vaccination>", methods=["PUT"])
def route_modifier_vaccination(id_vaccination):
    data = request.json
    vaccination = modifier_vaccination(id_vaccination, utilisateur=current_user, **data)
    if vaccination:
        return jsonify({"message": "Vaccination modifiée", "id": vaccination.id_vaccination})
    return jsonify({"error": "Modification échouée"}), 400

@vaccination_bp.route("/supprimer/<int:id_vaccination>", methods=["DELETE"])
def route_supprimer_vaccination(id_vaccination):
    vaccination = supprimer_vaccination(id_vaccination, utilisateur=current_user)
    if vaccination:
        return jsonify({"message": "Vaccination supprimée"})
    return jsonify({"error": "Suppression échouée"}), 404
