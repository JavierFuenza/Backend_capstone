from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Usuario
from sqlalchemy.exc import SQLAlchemyError

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


@app.get(
    "/",
    summary="Saludo y lista de usuarios",
    description="""
Retorna un mensaje de saludo general y una lista de todos los usuarios registrados,
indicando su nombre y sueldo para demostrar la conexion a la base de datos.
"""
)
def test(db: Session = Depends(get_db)):
    try:
        usuarios = db.query(Usuario).all()
        lista_usuarios = [f"{u.nombre} que gana {u.sueldo}" for u in usuarios]
    except SQLAlchemyError:
        # Si hay un error de conexión a la BD, devolver mensaje por defecto
        lista_usuarios = []
    
    return {
        "mensaje": "Hola desde FastAPI con docker en Render conectado con Neon PostgreSQL",
        "saludos_especiales": lista_usuarios,
        "nota": "Si la base de datos no responde, la lista estará vacía"
    }

