from flask import Blueprint, jsonify, request
from database.mysql_connection import SessionLocal
from models.enfant import Enfant
from models.vaccin import Vaccin
from models.vaccination import Vaccination
from datetime import datetime
from utils.authorization import role_required
from flask_login import current_user

analyse_bp = Blueprint("analyse", __name__)

def calculer_age(date_naissance):
    naissance = datetime.strptime(str(date_naissance), "%Y-%m-%d")
    today = datetime.today()
    return (today.year - naissance.year) - ((today.month, today.day) < (naissance.month, naissance.day))

@analyse_bp.route("/enfants-a-jour", methods=["GET"])
@role_required(["admin", "médecin"])
def enfants_a_jour():
    utilisateur = current_user
    db = SessionLocal()
    enfants = db.query(Enfant).all()
    vaccins = db.query(Vaccin).all()
    vaccinations = db.query(Vaccination).all()
    resultats = []
    for enfant in enfants:
        age = calculer_age(enfant.date_naissance)
        vaccins_requis = [v for v in vaccins if v.age_recommande <= age]
        vaccins_faits = [v.vaccin_id for v in vaccinations if v.id_enfant == enfant.id_enfant]
        est_a_jour = all(v.vaccin_id in vaccins_faits for v in vaccins_requis)
        if est_a_jour:
            resultats.append({
                "id": enfant.id_enfant,
                "prenom": enfant.prenom,
                "nom": enfant.nom
            })
    db.close()
    return jsonify(resultats)

@analyse_bp.route("/enfants-en-retard", methods=["GET"])
@role_required(["admin", "médecin"])
def enfants_en_retard():
    utilisateur = current_user
    db = SessionLocal()
    enfants = db.query(Enfant).all()
    vaccins = db.query(Vaccin).all()
    vaccinations = db.query(Vaccination).all()
    resultats = []
    for enfant in enfants:
        age = calculer_age(enfant.date_naissance)
        vaccins_requis = [v for v in vaccins if v.age_recommande <= age]
        vaccins_faits = [v.vaccin_id for v in vaccinations if v.id_enfant == enfant.id_enfant]
        en_retard = any(v.vaccin_id not in vaccins_faits for v in vaccins_requis)
        if en_retard:
            resultats.append({
                "id": enfant.id_enfant,
                "prenom": enfant.prenom,
                "nom": enfant.nom
            })
    db.close()
    return jsonify(resultats)

@analyse_bp.route("/vaccins-manquants/<int:id_enfant>", methods=["GET"])
@role_required(["admin", "médecin"])
def vaccins_manquants(id_enfant):
    utilisateur = current_user
    db = SessionLocal()
    enfant = db.query(Enfant).filter_by(id_enfant=id_enfant).first()
    if not enfant:
        db.close()
        return jsonify({"error": "Enfant non trouvé"}), 404
    age = calculer_age(enfant.date_naissance)
    vaccins = db.query(Vaccin).filter(Vaccin.age_recommande <= age).all()
    vaccinations = db.query(Vaccination).filter_by(id_enfant=id_enfant).all()
    vaccins_faits_ids = [v.vaccin_id for v in vaccinations]
    manquants = [{"vaccin_id": v.vaccin_id, "nom": v.nom_vaccin} for v in vaccins if v.vaccin_id not in vaccins_faits_ids]
    db.close()
    return jsonify({
        "enfant": {
            "id": enfant.id_enfant,
            "prenom": enfant.prenom,
            "nom": enfant.nom
        },
        "vaccins_manquants": manquants
    })

@analyse_bp.route("/statistiques", methods=["GET"])
@role_required(["admin", "médecin"])
def statistiques():
    utilisateur = current_user
    db = SessionLocal()
    total_enfants = db.query(Enfant).count()
    total_vaccins = db.query(Vaccin).count()
    total_vaccinations = db.query(Vaccination).count()
    db.close()
    return jsonify({
        "total_enfants": total_enfants,
        "total_vaccins": total_vaccins,
        "total_vaccinations": total_vaccinations
    })