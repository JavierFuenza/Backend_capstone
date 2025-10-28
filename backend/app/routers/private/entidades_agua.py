from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from core.dependencies import get_db
from models.entidades_agua import EntidadAgua
from schemas.entidades_agua import EntidadAguaSchema

# Importar todos los modelos de agua
from models.agua import (
    VMarMensual,
    VGlaciaresAnualCuenca,
    VColiformesFecalesEnMatrizBiologica,
    VColiformesFecalesEnMatrizAcuosa,
    VMetalesTotalesEnLaMatrizSedimentaria,
    VMetalesDisueltosEnLaMatrizAcuosa,
    VCaudalMedioDeAguasCorrientes,
    VCantidadDeAguaCaida,
    VEvaporacionRealPorEstacion,
    VVolumenDelEmbalsePorEmbalse,
    VAlturaNieveEquivalenteEnAgua,
    VNivelEstaticoDeAguasSubterraneas
)

# Importar todos los schemas de agua
from schemas.agua import (
    MarMensualSchema,
    GlaciaresAnualCuencaSchema,
    ColiformesBiologicaSchema,
    ColiformesAcuosaSchema,
    MetalesSedimentariaSchema,
    MetalesAcuosaSchema,
    CaudalSchema,
    LluviaSchema,
    EvaporacionSchema,
    EmbalseSchema,
    NieveSchema,
    PozoSchema
)

router = APIRouter(
    prefix="/entidades-agua",
    tags=["Entidades de Agua"],
    responses={404: {"description": "No encontrado"}}
)

# Mapeo de tipos a modelos y columnas de estación
TIPO_VISTA_MAPPING: Dict[str, Dict[str, Any]] = {
    "Cuenca Hidrográfica": {
        "model": VGlaciaresAnualCuenca,
        "schema": GlaciaresAnualCuencaSchema,
        "estacion_column": "estacion"
    },
    "Embalse": {
        "model": VVolumenDelEmbalsePorEmbalse,
        "schema": EmbalseSchema,
        "estacion_column": "embalse"
    },
    "Pozo de Monitoreo": {
        "model": VNivelEstaticoDeAguasSubterraneas,
        "schema": PozoSchema,
        "estacion_column": "estaciones_pozo"
    },
    "Estación Nivométrica": {
        "model": VAlturaNieveEquivalenteEnAgua,
        "schema": NieveSchema,
        "estacion_column": "estaciones_nivometricas"
    },
    "Estación Costera - Coliformes Biológicos": {
        "model": VColiformesFecalesEnMatrizBiologica,
        "schema": ColiformesBiologicaSchema,
        "estacion_column": "estaciones_poal"
    },
    "Estación de Evaporación": {
        "model": VEvaporacionRealPorEstacion,
        "schema": EvaporacionSchema,
        "estacion_column": "estacion"
    },
    "Estación Meteorológica": {
        "model": VCantidadDeAguaCaida,
        "schema": LluviaSchema,
        "estacion_column": "estaciones_meteorologicas_dmc"
    },
    "Estación Oceanográfica": {
        "model": VMarMensual,
        "schema": MarMensualSchema,
        "estacion_column": "estacion"
    },
    "Estación Costera - Coliformes Acuosos": {
        "model": VColiformesFecalesEnMatrizAcuosa,
        "schema": ColiformesAcuosaSchema,
        "estacion_column": "estaciones_poal"
    },
    "Estación Costera - Metales Disueltos": {
        "model": VMetalesDisueltosEnLaMatrizAcuosa,
        "schema": MetalesAcuosaSchema,
        "estacion_column": "estaciones_poal"
    },
    "Estación Fluviométrica": {
        "model": VCaudalMedioDeAguasCorrientes,
        "schema": CaudalSchema,
        "estacion_column": "estaciones_fluviometricas"
    },
    "Estación Costera - Metales Sedimentos": {
        "model": VMetalesTotalesEnLaMatrizSedimentaria,
        "schema": MetalesSedimentariaSchema,
        "estacion_column": "estaciones_poal"
    }
}

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

@router.get("/metricas/{nombre_estacion}", response_model=List[str])
async def get_metricas_by_estacion(
    nombre_estacion: str,
    db: Session = Depends(get_db)
):
    """
    Obtener las métricas (tipos) asociadas a una estación específica por su nombre.

    Una estación puede estar asociada a múltiples tipos (métricas), este endpoint
    retorna todos los tipos únicos vinculados a la estación especificada.

    Args:
        nombre_estacion (str): Nombre de la estación de agua

    Returns:
        List[str]: Lista de tipos (métricas) asociados a la estación, ordenados alfabéticamente

    Raises:
        HTTPException 404: Si no se encuentra ninguna estación con ese nombre

    Ejemplo de uso:
        GET /entidades-agua/metricas/Estación%20Mapocho%20Alto

    Ejemplo de respuesta:
        [
            "caudal",
            "calidad",
            "temperatura"
        ]
    """
    # Buscar todas las entidades con ese nombre
    metricas = db.query(EntidadAgua.tipo).filter(
        EntidadAgua.nombre == nombre_estacion
    ).distinct().order_by(EntidadAgua.tipo).all()

    if not metricas:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron métricas para la estación '{nombre_estacion}'"
        )

    return [metrica[0] for metrica in metricas]

@router.get("/datos/{nombre_estacion}/{tipo}")
async def get_datos_estacion_por_tipo(
    nombre_estacion: str,
    tipo: str,
    db: Session = Depends(get_db)
):
    """
    Obtener los datos de una estación específica desde la vista asociada al tipo (métrica).

    Este endpoint busca los datos de una estación en la vista correspondiente según el tipo
    de métrica solicitado. Cada tipo de métrica está asociado a una vista específica en la base de datos.

    Args:
        nombre_estacion (str): Nombre de la estación de agua
        tipo (str): Tipo de métrica/vista a consultar (debe ser exactamente como aparece en la base de datos)

    Tipos disponibles:
        - Cuenca Hidrográfica: Datos anuales de glaciares por cuenca
        - Embalse: Volumen de embalse
        - Pozo de Monitoreo: Nivel estático de aguas subterráneas
        - Estación Nivométrica: Altura de nieve equivalente en agua
        - Estación Costera - Coliformes Biológicos: Coliformes fecales en matriz biológica
        - Estación de Evaporación: Evaporación real por estación
        - Estación Meteorológica: Cantidad de agua caída (precipitación)
        - Estación Oceanográfica: Datos mensuales del mar (temperatura, nivel)
        - Estación Costera - Coliformes Acuosos: Coliformes fecales en matriz acuosa
        - Estación Costera - Metales Disueltos: Metales disueltos en matriz acuosa
        - Estación Fluviométrica: Caudal medio de aguas corrientes
        - Estación Costera - Metales Sedimentos: Metales totales en matriz sedimentaria

    Returns:
        List: Lista de registros con los datos de la estación para el tipo especificado

    Raises:
        HTTPException 400: Si el tipo no es válido
        HTTPException 404: Si no se encuentran datos para la estación y tipo especificados

    Ejemplo de uso:
        GET /entidades-agua/datos/Estación%20Mapocho/Estación%20Fluviométrica

    Ejemplo de respuesta:
        [
            {
                "mes": "2024-01",
                "aguas_corrientes": "Río Mapocho",
                "estaciones_fluviometricas": "Estación Mapocho",
                "value": 15.5
            }
        ]
    """
    # Validar que el tipo existe en el mapeo
    if tipo not in TIPO_VISTA_MAPPING:
        tipos_disponibles = ", ".join(TIPO_VISTA_MAPPING.keys())
        raise HTTPException(
            status_code=400,
            detail=f"Tipo '{tipo}' no válido. Tipos disponibles: {tipos_disponibles}"
        )

    # Obtener configuración del tipo
    config = TIPO_VISTA_MAPPING[tipo]
    model = config["model"]
    schema = config["schema"]
    estacion_column = config["estacion_column"]

    # Obtener el atributo de columna del modelo
    estacion_attr = getattr(model, estacion_column)

    # Consultar la vista correspondiente
    datos = db.query(model).filter(
        estacion_attr == nombre_estacion
    ).all()

    if not datos:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron datos para la estación '{nombre_estacion}' en la vista de tipo '{tipo}'"
        )

    # Convertir a schema para retornar con el formato correcto
    return [schema.from_orm(dato) for dato in datos]
