from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#conection to the db created via docker
engine = create_engine("mysql+pymysql://user:user@sql/Proyecto_Fase_1")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()