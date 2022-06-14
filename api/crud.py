from . import models, database

def get_db():
    try:
        db = database.SessionLocal()
        yield db
    finally:
        db.close()