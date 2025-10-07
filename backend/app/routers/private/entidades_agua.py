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
    Obtener todas las entidades de agua registradas en el sistema.

    Este endpoint retorna un listado completo de todas las entidades hídricas,
    incluyendo estaciones de monitoreo, cuencas, embalses, pozos, ríos, etc.

    Returns:
        List[EntidadAguaSchema]: Lista de entidades ordenadas por tipo y nombre

    Ejemplo de respuesta:
        [
            {
                "id": 1,
                "nombre": "Estación Mapocho Alto",
                "tipo": "estacion",
                "descripcion": "Estación de monitoreo en cuenca alta",
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        ]
    """
    entidades = db.query(EntidadAgua).order_by(EntidadAgua.tipo, EntidadAgua.nombre).all()
    return entidades

@router.get("/tipo/{tipo}", response_model=List[EntidadAguaSchema])
async def get_entidades_by_tipo(
    tipo: str,
    db: Session = Depends(get_db)
):
    """
    Obtener entidades de agua filtradas por tipo específico.

    Permite filtrar las entidades hídricas según su clasificación (tipo).
    Útil para obtener solo estaciones, cuencas, embalses, etc.

    Args:
        tipo (str): Tipo de entidad a filtrar

    Tipos disponibles:
        - estacion: Estaciones de monitoreo
        - cuenca: Cuencas hidrográficas
        - embalse: Embalses y represas
        - pozo: Pozos de agua subterránea
        - rio: Ríos y afluentes
        - lago: Lagos y lagunas
        - canal: Canales de riego o distribución

    Returns:
        List[EntidadAguaSchema]: Lista de entidades del tipo especificado, ordenadas por nombre

    Raises:
        HTTPException 404: Si no existen entidades del tipo solicitado

    Ejemplo de uso:
        GET /entidades-agua/tipo/estacion

    Ejemplo de respuesta:
        [
            {
                "id": 5,
                "nombre": "Estación Río Maipo",
                "tipo": "estacion",
                "descripcion": "Monitoreo de caudal y calidad",
                "created_at": "2024-02-01T08:00:00",
                "updated_at": "2024-02-01T08:00:00"
            }
        ]
    """
    entidades = db.query(EntidadAgua).filter(
        EntidadAgua.tipo == tipo
    ).order_by(EntidadAgua.nombre).all()

    if not entidades:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron entidades del tipo '{tipo}'"
        )

    return entidades

@router.get("/tipos", response_model=List[str])
async def get_tipos_disponibles(db: Session = Depends(get_db)):
    """
    Obtener catálogo de todos los tipos de entidades de agua disponibles.

    Este endpoint retorna una lista única de todos los tipos de entidades
    que están actualmente registrados en la base de datos, sin duplicados.

    Returns:
        List[str]: Lista de tipos únicos, ordenados alfabéticamente

    Casos de uso:
        - Poblar dropdowns/selects dinámicos en el frontend
        - Validar tipos antes de crear nuevas entidades
        - Conocer la taxonomía de entidades hídricas disponibles
        - Generar filtros dinámicos en interfaces de usuario

    Ejemplo de respuesta:
        [
            "canal",
            "cuenca",
            "embalse",
            "estacion",
            "lago",
            "pozo",
            "rio"
        ]

    Note:
        La lista se genera dinámicamente basándose en los datos existentes,
        por lo que puede variar según el contenido de la base de datos.
    """
    tipos = db.query(EntidadAgua.tipo).distinct().order_by(EntidadAgua.tipo).all()
    return [tipo[0] for tipo in tipos]
