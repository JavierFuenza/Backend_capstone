from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from core.dependencies import get_db
from models.estaciones import Estacion
from schemas.estaciones import EstacionSchema

router = APIRouter(
    prefix="/estaciones",
    tags=["Estaciones"],
    responses={404: {"description": "No encontrado"}}
)

@router.get("/", response_model=List[EstacionSchema])
async def get_all_estaciones(
    db: Session = Depends(get_db),
    numero_region: Optional[int] = Query(None, description="Filtrar por número de región")
):
    """Obtener todas las estaciones. Opcionalmente filtrar por región."""
    query = db.query(Estacion)

    if numero_region is not None:
        query = query.filter(Estacion.numero_region == numero_region)

    estaciones = query.order_by(Estacion.nombre).all()
    return estaciones

@router.get("/{estacion_id}", response_model=EstacionSchema)
async def get_estacion_by_id(estacion_id: int, db: Session = Depends(get_db)):
    """Obtener una estación específica por ID"""
    estacion = db.query(Estacion).filter(Estacion.id == estacion_id).first()
    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no encontrada")
    return estacion

@router.get("/nombre/{nombre}", response_model=EstacionSchema)
async def get_estacion_by_nombre(nombre: str, db: Session = Depends(get_db)):
    """Obtener una estación específica por nombre exacto"""
    estacion = db.query(Estacion).filter(Estacion.nombre == nombre).first()
    if not estacion:
        raise HTTPException(status_code=404, detail=f"Estación '{nombre}' no encontrada")
    return estacion
