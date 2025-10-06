from database.mysql_connection import engine
from sqlalchemy.sql import text

# Enfants dont les vaccins sont tous à jour
def enfants_a_jour():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT e.id_enfant, e.prenom, e.nom
            FROM enfants e
            WHERE NOT EXISTS (
              SELECT 1
              FROM vaccinations v
              JOIN vaccins vc ON vc.vaccin_id = v.vaccin_id
              WHERE v.id_enfant = e.id_enfant
              AND v.statut_vaccination != 'à jour'
            );
        """))
        return result.fetchall()


# Enfants en retard de vaccination
def enfants_en_retard():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT e.id_enfant, e.prenom, e.nom, vc.nom_vaccin, v.statut_vaccination
            FROM enfants e
            JOIN vaccinations v ON v.id_enfant = e.id_enfant
            JOIN vaccins vc ON vc.vaccin_id = v.vaccin_id
            WHERE v.statut_vaccination = 'en retard';
        """))
        return result.fetchall()


# Vaccins recommandés non encore faits selon l'âge
def vaccins_manquants():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT e.id_enfant, e.prenom, e.date_naissance, vc.nom_vaccin
            FROM enfants e
            JOIN vaccins vc
            WHERE TIMESTAMPDIFF(MONTH, e.date_naissance, CURDATE()) >= vc.age_recommande
            AND NOT EXISTS (
                SELECT 1 FROM vaccinations v
                WHERE v.id_enfant = e.id_enfant AND v.vaccin_id = vc.vaccin_id
            );
        """))
        return result.fetchall()
