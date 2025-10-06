from database.mysql_connection import SessionLocal
from models.enfant import Enfant
import traceback
from utils.authorization import role_required
from flask_login import current_user

@role_required(["admin", "médecin"])
def ajouter_enfant(prenom, nom, sexe, date_naissance, historique, utilisateur=None):
    try:
        db = SessionLocal()
        enfant = Enfant(
            prenom=prenom,
            nom=nom,
            sexe=sexe,
            date_naissance=date_naissance,
            historique_medical=historique
        )
        db.add(enfant)
        db.commit()
        db.refresh(enfant)
        return enfant
    except Exception as e:
        print("❌ ERREUR - ajout enfant :")
        traceback.print_exc()
        return None
    finally:
        db.close()

@role_required(["admin", "médecin", "parent"])
def lister_enfants(utilisateur=None):
    db = SessionLocal()
    if utilisateur and hasattr(utilisateur, 'role') and utilisateur.role == 'parent':
        enfants = db.query(Enfant).filter_by(parent_id=utilisateur.id_utilisateur).all()
    else:
        enfants = db.query(Enfant).all()
    db.close()
    return enfants

@role_required(["admin", "médecin", "parent"])
def get_enfant(id_enfant, utilisateur=None):
    db = SessionLocal()
    enfant = db.query(Enfant).filter_by(id_enfant=id_enfant).first()
    db.close()
    return enfant

@role_required(["admin", "médecin"])
def modifier_enfant(id_enfant, utilisateur=None, **kwargs):
    db = SessionLocal()
    enfant = db.query(Enfant).filter_by(id_enfant=id_enfant).first()
    if enfant:
        for key, value in kwargs.items():
            setattr(enfant, key, value)
        db.commit()
        db.refresh(enfant)
    db.close()
    return enfant

@role_required(["admin"])
def supprimer_enfant(id_enfant, utilisateur=None):
    db = SessionLocal()
    enfant = db.query(Enfant).filter_by(id_enfant=id_enfant).first()
    if enfant:
        db.delete(enfant)
        db.commit()
    db.close()
    return enfant
