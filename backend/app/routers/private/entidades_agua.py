from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from core.dependencies import get_db
from models.entidades_agua import EntidadAgua
from schemas.entidades_agua import EntidadAguaSchema

router = APIRouter(
    prefix="/entidades-agua",
    tags=["Entidades de Agua"],
    responses={404: {"description": "No encontrado"}}
)

@router.get("/", response_model=List[EntidadAguaSchema])
async def get_all_entidades_agua(db: Session = Depends(get_db)):
    """
    Obtener todas las entidades de agua (estaciones, cuencas, embalses, etc.)
    """
    entidades = db.query(EntidadAgua).order_by(EntidadAgua.subtipo, EntidadAgua.nombre).all()
    return entidades

@router.get("/subtipo/{subtipo}", response_model=List[EntidadAguaSchema])
async def get_entidades_by_subtipo(
    subtipo: str,
    db: Session = Depends(get_db)
):
    """
    Obtener todas las entidades de agua de un subtipo específico

    Ejemplos de subtipos:
    - estacion
    - cuenca
    - embalse
    - pozo
    - rio
    - etc.
    """
    entidades = db.query(EntidadAgua).filter(
        EntidadAgua.subtipo == subtipo
    ).order_by(EntidadAgua.nombre).all()

    if not entidades:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron entidades del subtipo '{subtipo}'"
        )

    return entidades

@router.get("/subtipos", response_model=List[str])
async def get_subtipos_disponibles(db: Session = Depends(get_db)):
    """
    Obtener lista de todos los subtipos disponibles en la tabla

    Útil para:
    - Poblar dropdowns/selects en el frontend
    - Conocer qué tipos de entidades existen en la base de datos
    """
    subtipos = db.query(EntidadAgua.subtipo).distinct().order_by(EntidadAgua.subtipo).all()
    return [subtipo[0] for subtipo in subtipos]
