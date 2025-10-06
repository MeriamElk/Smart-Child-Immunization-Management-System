from datetime import datetime
from vaccination_backend import db

class Enfant(db.Model):
    __tablename__ = 'enfants'
    
    id_enfant = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    sexe = db.Column(db.String(1))  # 'M' ou 'F'
    date_naissance = db.Column(db.Date, nullable=False)
    historique_medical = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id_utilisateur'))
    
    # Relations
    vaccinations = db.relationship("Vaccination", backref="enfant", cascade="all, delete", passive_deletes=True)
    alertes = db.relationship("Alerte", backref="enfant", cascade="all, delete", passive_deletes=True)

    
    def __init__(self, prenom, nom, date_naissance, sexe=None, historique_medical=None, parent_id=None):
        self.prenom = prenom
        self.nom = nom
        self.date_naissance = date_naissance
        self.sexe = sexe
        self.historique_medical = historique_medical
        self.parent_id = parent_id
    
    def to_dict(self):
        return {
            'id': self.id_enfant,
            'prenom': self.prenom,
            'nom': self.nom,
            'date_naissance': self.date_naissance.isoformat() if self.date_naissance else None,
            'sexe': self.sexe,
            'historique_medical': self.historique_medical
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def get_by_id(id):
        return Enfant.query.get(id)
