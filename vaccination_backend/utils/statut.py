from datetime import datetime, timedelta
from vaccination_backend import db
from vaccination_backend.models.vaccin import Vaccin

def mettre_a_jour_statut_vaccination(vaccination):
    vaccin = db.session.get(Vaccin, vaccination.vaccin_id)
    nb_doses = vaccin.nombre_doses

    if vaccination.dose < nb_doses:
        prochaine_date = vaccination.date_vaccination + timedelta(days=30 * vaccination.dose)
        if datetime.today().date() > prochaine_date:
            vaccination.statut_vaccination = 'en retard'
        else:
            vaccination.statut_vaccination = 'à jour'
    else:
        vaccination.statut_vaccination = 'à jour'
