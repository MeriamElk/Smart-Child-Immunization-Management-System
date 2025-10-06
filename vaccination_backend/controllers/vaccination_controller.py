from database.mysql_connection import SessionLocal
from models.vaccination import Vaccination
import traceback
from utils.authorization import role_required

@role_required(["admin", "médecin"])
def enregistrer_vaccination(id_enfant, vaccin_id, dose, statut, utilisateur=None):
    try:
        db = SessionLocal()
        vaccination = Vaccination(
            id_enfant=id_enfant,
            vaccin_id=vaccin_id,
            dose=dose,
            statut_vaccination=statut
        )
        db.add(vaccination)
        db.commit()
        db.refresh(vaccination)
        return vaccination
    except Exception as e:
        print("❌ ERREUR - ajout vaccination :")
        traceback.print_exc()
        return None
    finally:
        db.close()

@role_required(["admin", "médecin"])
def get_vaccination(id_vaccination, utilisateur=None):
    db = SessionLocal()
    vaccination = db.query(Vaccination).filter_by(id_vaccination=id_vaccination).first()
    db.close()
    return vaccination

@role_required(["admin", "médecin"])
def lister_vaccinations(utilisateur=None):
    db = SessionLocal()
    vaccinations = db.query(Vaccination).all()
    db.close()
    return vaccinations

@role_required(["admin", "médecin"])
def modifier_vaccination(id_vaccination, utilisateur=None, **kwargs):
    db = SessionLocal()
    vaccination = db.query(Vaccination).filter_by(id_vaccination=id_vaccination).first()
    if vaccination:
        for key, value in kwargs.items():
            setattr(vaccination, key, value)
        db.commit()
        db.refresh(vaccination)
    db.close()
    return vaccination

@role_required(["admin"])
def supprimer_vaccination(id_vaccination, utilisateur=None):
    db = SessionLocal()
    vaccination = db.query(Vaccination).filter_by(id_vaccination=id_vaccination).first()
    if vaccination:
        db.delete(vaccination)
        db.commit()
    db.close()
    return vaccination
