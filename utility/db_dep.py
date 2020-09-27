from database.base import SessionLocal


def get_db():
    db = SessionLocal()
    yield db
    db.close()
