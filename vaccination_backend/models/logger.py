from database.mongodb_connection import logs_collection
from datetime import datetime

class Logger:
    @staticmethod
    def log_action(id_utilisateur, action, details):
        log_entry = {
            "id_utilisateur": id_utilisateur,
            "action": action,
            "date_action": datetime.now(),
            "details": details
        }
        logs_collection.insert_one(log_entry)
