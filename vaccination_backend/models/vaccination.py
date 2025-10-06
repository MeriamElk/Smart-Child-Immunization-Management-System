from datetime import datetime
from vaccination_backend import db

class Vaccination(db.Model):
    __tablename__ = 'vaccinations'
    
    id_vaccination = db.Column(db.Integer, primary_key=True)
    id_enfant = db.Column(db.Integer, db.ForeignKey('enfants.id_enfant'), nullable=False)
    vaccin_id = db.Column(db.Integer, db.ForeignKey('vaccins.vaccin_id'), nullable=False)
    date_vaccination = db.Column(db.Date, nullable=False)
    dose = db.Column(db.Integer, default=1)
    statut_vaccination = db.Column(db.String(20), default='à jour')  # 'à jour' ou 'en retard'
    
    def __init__(self, id_enfant, vaccin_id, date_vaccination, dose=1, statut_vaccination='à jour'):
        self.id_enfant = id_enfant
        self.vaccin_id = vaccin_id
        self.date_vaccination = date_vaccination
        self.dose = dose
        self.statut_vaccination = statut_vaccination
    
    def to_dict(self):
        return {
            'id': self.id_vaccination,
            'id_enfant': self.id_enfant,
            'vaccin_id': self.vaccin_id,
            'date_vaccination': self.date_vaccination.isoformat() if self.date_vaccination else None,
            'dose': self.dose,
            'statut_vaccination': self.statut_vaccination
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def get_by_id(id):
        return Vaccination.query.get(id)
    
    @staticmethod
    def get_by_enfant(enfant_id):
        return Vaccination.query.filter_by(id_enfant=enfant_id).all()
    
    @staticmethod
    def get_by_vaccin(vaccin_id):
        return Vaccination.query.filter_by(vaccin_id=vaccin_id).all()
