from sqlalchemy                 import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm             import sessionmaker
from core.config                import Settings

# Server Setting
settings = Settings()

# TODO : MariaDB URL
MARIADB_DATABASE_URL = "mariadb+mariadbconnector://" + settings.DB_USER + ":" + settings.DB_PASS + "@" + settings.DB_HOST + ":" + settings.DB_PORT + "/FlightRecord"
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# engine = create_engine(MARIADB_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()