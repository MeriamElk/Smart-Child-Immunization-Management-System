from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

print("🔥 mysql_connection.py chargé")

DATABASE_URL = "mysql+pymysql://root:Gds20242025@localhost:3306/vaccination_db"

engine = create_engine(DATABASE_URL)
try:
    # tester la connexion MySQL immédiatement
    with engine.connect() as conn:
        print("✅ Connexion MySQL réussie")
except Exception as e:
    print("❌ Erreur de connexion MySQL :", e)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
