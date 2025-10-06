from database.mysql_connection import SessionLocal
from models.utilisateur import Utilisateur
import traceback
from utils.authorization import role_required

@role_required(["admin"])
def ajouter_utilisateur(email, role, mot_de_passe, utilisateur=None):
    try:
        db = SessionLocal()
        if db.query(Utilisateur).filter_by(email=email).first():
            print("⚠️ Utilisateur déjà existant.")
            return None

        utilisateur = Utilisateur(email=email, role=role)
        utilisateur.set_password(mot_de_passe)
        db.add(utilisateur)
        db.commit()
        db.refresh(utilisateur)
        return utilisateur
    except Exception as e:
        print("❌ ERREUR - ajout utilisateur :")
        traceback.print_exc()
        return None
    finally:
        db.close()

@role_required(["admin", "médecin"])
def get_utilisateur(email, utilisateur=None):
    db = SessionLocal()
    utilisateur = db.query(Utilisateur).filter_by(email=email).first()
    db.close()
    return utilisateur

@role_required(["admin"])
def modifier_utilisateur(id_utilisateur, utilisateur=None, **kwargs):
    db = SessionLocal()
    utilisateur = db.query(Utilisateur).filter_by(id_utilisateur=id_utilisateur).first()
    if utilisateur:
        for key, value in kwargs.items():
            setattr(utilisateur, key, value)
        db.commit()
        db.refresh(utilisateur)
    db.close()
    return utilisateur

@role_required(["admin"])
def supprimer_utilisateur(id_utilisateur, utilisateur=None):
    db = SessionLocal()
    utilisateur = db.query(Utilisateur).filter_by(id_utilisateur=id_utilisateur).first()
    if utilisateur:
        db.delete(utilisateur)
        db.commit()
    db.close()
    return utilisateur
