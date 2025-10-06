print("✅ Lancement du backend vaccination")

from database.mysql_connection import Base, engine
from controllers.utilisateur_controller import ajouter_utilisateur
from controllers.enfant_controller import ajouter_enfant
from controllers.vaccin_controller import ajouter_vaccin
from controllers.vaccination_controller import enregistrer_vaccination
from models.alerte import Alerte
from models.logger import Logger

# 1. Création des tables (MySQL)
Base.metadata.create_all(bind=engine)
print("🗂️  Tables MySQL créées (si non existantes)")

# 2. Création d’un utilisateur
utilisateur = ajouter_utilisateur("dr.nadia@hopital.ma", "médecin", "azerty123")
if utilisateur:
    print(f"👤 Utilisateur créé : {utilisateur.email}")
else:
    print("⚠️  Utilisateur non ajouté (existe déjà ?)")

# 3. Création d’un enfant
enfant = ajouter_enfant("Yasmine", "Bennani", "F", "2020-05-14", "Rien à signaler")
print(f"👶 Enfant ajouté : {enfant.prenom} {enfant.nom}")

# 4. Création d’un vaccin
vaccin = ajouter_vaccin(
    nom="ROR", age=12, doses=1,
    effets="Fièvre légère",
    type_vaccin="atténué",
    maladies="Rougeole, Oreillons, Rubéole"
)
print(f"💉 Vaccin ajouté : {vaccin.nom_vaccin}")

# 5. Enregistrement d’une vaccination
vaccination = enregistrer_vaccination(
    id_enfant=enfant.id_enfant,
    vaccin_id=vaccin.vaccin_id,
    dose=1,
    statut="à jour"
)
print("📋 Vaccination enregistrée.")

# 6. Création d’une alerte dans MongoDB
alerte = Alerte(id_enfant=enfant.id_enfant, vaccin_id=vaccin.vaccin_id, date_alerte="2025-06-01")
alerte.envoyer_alerte()
print("📢 Alerte de vaccination envoyée.")

# 7. Log de l’action
Logger.log_action(
    id_utilisateur=utilisateur.id_utilisateur,
    action="Ajout vaccination",
    details=f"{vaccin.nom_vaccin} pour {enfant.prenom} {enfant.nom}"
)
print("📝 Log enregistré dans MongoDB")
