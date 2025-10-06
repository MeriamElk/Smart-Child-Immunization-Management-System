from datetime import datetime
from vaccination_backend import db

class Vaccin(db.Model):
    __tablename__ = 'vaccins'
    
    vaccin_id = db.Column(db.Integer, primary_key=True)
    nom_vaccin = db.Column(db.String(100), nullable=False)
    age_recommande = db.Column(db.Integer)
    nombre_doses = db.Column(db.Integer, default=1)
    effets_secondaires = db.Column(db.Text)
    type_vaccin = db.Column(db.String(50))
    maladies_ciblees = db.Column(db.Text)

    vaccinations = db.relationship('Vaccination', backref='vaccin', lazy=True)

    def __init__(self, nom_vaccin, age_recommande=None, nombre_doses=1, effets_secondaires=None, type_vaccin=None, maladies_ciblees=None):
        self.nom_vaccin = nom_vaccin
        self.age_recommande = age_recommande
        self.nombre_doses = nombre_doses
        self.effets_secondaires = effets_secondaires
        self.type_vaccin = type_vaccin
        self.maladies_ciblees = maladies_ciblees
