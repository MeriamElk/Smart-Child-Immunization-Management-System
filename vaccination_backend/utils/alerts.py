# vaccination_backend/utils/alerts.py

from datetime import date, timedelta
from vaccination_backend import db
from vaccination_backend.models.vaccination import Vaccination
from vaccination_backend.models.vaccin import Vaccin
from vaccination_backend.models.alerte import Alerte

def verifier_et_creer_alertes():
    today = date.today()
    vaccinations = Vaccination.query.all()

    for v in vaccinations:
        vaccin = db.session.get(Vaccin, v.vaccin_id)
        if not vaccin:
            continue

        prochaine_dose = v.dose + 1
        if prochaine_dose <= vaccin.nombre_doses:
            date_echeance = v.date_vaccination + timedelta(days=30 * prochaine_dose)

            existe = Alerte.query.filter_by(
                enfant_id=v.id_enfant,
                titre=f"Rappel en retard ({vaccin.nom_vaccin})",
                statut='active'
            ).first()

            if not existe and today > date_echeance:
                alerte = Alerte(
                    type="rappel",
                    titre=f"Rappel en retard ({vaccin.nom_vaccin})",
                    description=f"La dose {prochaine_dose} du vaccin {vaccin.nom_vaccin} est en retard.",
                    date_alerte=today,
                    date_echeance=date_echeance,
                    statut='active',
                    enfant_id=v.id_enfant,
                    utilisateur_id=1
                )
                db.session.add(alerte)
    db.session.commit()
