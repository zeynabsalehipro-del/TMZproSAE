from psycopg2 import Error
from config_PostgreSQL import DB_CONFIG
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
def get_connection():
    #Crée et retourne une nouvelle connexion MySQL.
    #Lève une exception si la connexion échoue.
    try:
        arg_engine=f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        engine = create_engine(arg_engine)
        Session = sessionmaker(bind=engine)
        return Session()
    except Error as e:
        print(f"Erreur connexion PostgreSQL : {e}")
        raise
