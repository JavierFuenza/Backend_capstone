from fastapi import FastAPI
from database import SessionLocal, engine, Base

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Capstone Backend",
    version="0.1",
    description="""
API prototipo hecha con FastAPI + Docker + PostgreSQL (Neon) y hosteada en Render.
"""
)

# Dependencia para manejar la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()