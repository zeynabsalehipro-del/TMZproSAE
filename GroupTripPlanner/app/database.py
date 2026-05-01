import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base de données — lue depuis les variables d'environnement Docker.
# La valeur par défaut correspond à la configuration du docker-compose.yml.
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@db/TMZproSAE"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base commune à tous les modèles SQLAlchemy du projet
Base = declarative_base()
