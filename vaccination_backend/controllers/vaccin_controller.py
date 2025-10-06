from database.mysql_connection import SessionLocal
from models.vaccin import Vaccin
import traceback
from utils.authorization import role_required

@role_required(["admin", "médecin"])
def ajouter_vaccin(nom, age, doses, effets, type_vaccin, maladies, utilisateur=None):
    try:
        db = SessionLocal()
        vaccin = Vaccin(
            nom_vaccin=nom,
            age_recommande=age,
            nombre_doses=doses,
            effets_secondaires=effets,
            type_vaccin=type_vaccin,
            maladies_ciblees=maladies
        )
        db.add(vaccin)
        db.commit()
        db.refresh(vaccin)
        return vaccin
    except Exception as e:
        print("❌ ERREUR - ajout vaccin :")
        traceback.print_exc()
        return None
    finally:
        db.close()

@role_required(["admin", "médecin", "parent"])
def lister_vaccins(utilisateur=None):
    db = SessionLocal()
    vaccins = db.query(Vaccin).all()
    db.close()
    return vaccins

@role_required(["admin", "médecin", "parent"])
def get_vaccin(vaccin_id, utilisateur=None):
    db = SessionLocal()
    vaccin = db.query(Vaccin).filter_by(vaccin_id=vaccin_id).first()
    db.close()
    return vaccin

@role_required(["admin", "médecin"])
def modifier_vaccin(vaccin_id, utilisateur=None, **kwargs):
    db = SessionLocal()
    vaccin = db.query(Vaccin).filter_by(vaccin_id=vaccin_id).first()
    if vaccin:
        for key, value in kwargs.items():
            setattr(vaccin, key, value)
        db.commit()
        db.refresh(vaccin)
    db.close()
    return vaccin

@role_required(["admin"])
def supprimer_vaccin(vaccin_id, utilisateur=None):
    db = SessionLocal()
    vaccin = db.query(Vaccin).filter_by(vaccin_id=vaccin_id).first()
    if vaccin:
        db.delete(vaccin)
        db.commit()
    db.close()
    return vaccin
