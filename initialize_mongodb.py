from pymongo import MongoClient
from datetime import datetime

# Connexion à MongoDB local
client = MongoClient("mongodb://localhost:27017/")
db = client["vaccination_db"]

# Créer les collections
alertes = db["alertes"]
logs = db["logs"]

# Insérer des documents d'exemple

# Alertes de vaccination
alertes.insert_many([
    {
        "id_enfant": 1,
        "vaccin_id": 3,
        "date_alerte": "2024-05-15",
        "type_alerte": "rappel",
        "statut_alerte": "en attente",
        "priorite": "haute"
    },
    {
        "id_enfant": 2,
        "vaccin_id": 4,
        "date_alerte": "2024-05-20",
        "type_alerte": "rappel",
        "statut_alerte": "envoyée",
        "priorite": "moyenne"
    }
])

# Logs utilisateur
logs.insert_many([
    {
        "id_utilisateur": 2,
        "action": "Ajout d'une vaccination",
        "date_action": datetime.now(),
        "details": "Vaccination contre la polio pour l’enfant 1"
    },
    {
        "id_utilisateur": 4,
        "action": "Connexion réussie",
        "date_action": datetime.now(),
        "details": "Admin connecté avec succès"
    }
])

print("✅ Collections alertes et logs créées avec données d'exemple.")
