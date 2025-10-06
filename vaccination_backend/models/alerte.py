from datetime import datetime
from vaccination_backend import db

class Alerte(db.Model):
    __tablename__ = 'alertes'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # 'vaccination', 'rappel', 'urgence'
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date_alerte = db.Column(db.DateTime, nullable=False)
    date_echeance = db.Column(db.DateTime)
    priorite = db.Column(db.String(20), default='normale')  # 'basse', 'normale', 'haute', 'urgence'
    statut = db.Column(db.String(20), default='active')  # 'active', 'resolue', 'annulee'
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Clés étrangères
    enfant_id = db.Column(db.Integer, db.ForeignKey('enfants.id_enfant'), nullable=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id_utilisateur'), nullable=False)
    
    def __init__(self, type, titre, date_alerte, enfant_id, utilisateur_id, description=None, date_echeance=None, priorite='normale', statut='active'):
        self.type = type
        self.titre = titre
        self.date_alerte = date_alerte
        self.enfant_id = enfant_id
        self.utilisateur_id = utilisateur_id
        self.description = description
        self.date_echeance = date_echeance
        self.priorite = priorite
        self.statut = statut
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'titre': self.titre,
            'description': self.description,
            'date_alerte': self.date_alerte.isoformat() if self.date_alerte else None,
            'date_echeance': self.date_echeance.isoformat() if self.date_echeance else None,
            'priorite': self.priorite,
            'statut': self.statut,
            'enfant_id': self.enfant_id,
            'utilisateur_id': self.utilisateur_id,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def get_by_id(id):
        return Alerte.query.get(id)
    
    @staticmethod
    def get_by_enfant(enfant_id):
        return Alerte.query.filter_by(enfant_id=enfant_id).all()
    
    @staticmethod
    def get_by_utilisateur(utilisateur_id):
        return Alerte.query.filter_by(utilisateur_id=utilisateur_id).all()
    
    @staticmethod
    def get_alertes_actives():
        return Alerte.query.filter_by(statut='active').all()
