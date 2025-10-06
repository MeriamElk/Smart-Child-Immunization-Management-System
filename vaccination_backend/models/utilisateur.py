from datetime import datetime
from vaccination_backend import db
import bcrypt

class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'
    
    id_utilisateur = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum('parent', 'médecin', 'admin'), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    
    # Relations
    alertes = db.relationship('Alerte', backref='utilisateur', lazy=True)
    
    def __init__(self, email, role, mot_de_passe=None):
        self.email = email
        self.role = role
        if mot_de_passe:
            self.set_password(mot_de_passe)
    
    def set_password(self, plain_password):
        self.mot_de_passe = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, plain_password):
        return self.mot_de_passe == plain_password
    
    def to_dict(self):
        return {
            'id': self.id_utilisateur,
            'email': self.email,
            'role': self.role
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def role_normalized(self):
        return self.role.lower().replace("é", "e")

    
    @staticmethod
    def get_by_id(id):
        return Utilisateur.query.get(id)
    
    @staticmethod
    def get_by_email(email):
        return Utilisateur.query.filter_by(email=email).first()

    def afficher_role(self):
        return f"Rôle : {self.role}"

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id_utilisateur)

from vaccination_backend.models.alerte import Alerte
