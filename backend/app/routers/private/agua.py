from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from core.dependencies import get_db
from models.agua import *
from schemas.agua import *

# Crear sub-routers para organizar endpoints por categoría
vistas_router = APIRouter(
    prefix="/agua/vistas",
    tags=["Agua - Vistas Generales"],
    responses={404: {"description": "No encontrado"}}
)

contaminantes_router = APIRouter(
    prefix="/agua/contaminantes",
    tags=["Agua - Contaminantes"],
    responses={404: {"description": "No encontrado"}}
)

hidrologia_router = APIRouter(
    prefix="/agua/hidrologia",
    tags=["Agua - Hidrología"],
    responses={404: {"description": "No encontrado"}}
)

meteorologicos_router = APIRouter(
    prefix="/agua/meteorologicos",
    tags=["Agua - Meteorológicos"],
    responses={404: {"description": "No encontrado"}}
)

almacenamiento_router = APIRouter(
    prefix="/agua/almacenamiento",
    tags=["Agua - Almacenamiento"],
    responses={404: {"description": "No encontrado"}}
)

# Router principal para incluir en main.py
router = APIRouter()

# ============================
# Vistas (devuelven toda la tabla)
# ============================

@vistas_router.get("/mar-mensual", response_model=List[MarMensualSchema])
async def get_mar_mensual(db: Session = Depends(get_db)):
    """Obtener todos los datos mensuales del mar - Vista completa"""
    data = db.query(VMarMensual).all()
    return data

@vistas_router.get("/glaciares-anual-cuenca", response_model=List[GlaciaresAnualCuencaSchema])
async def get_glaciares_anual_cuenca(db: Session = Depends(get_db)):
    """Obtener todos los datos anuales de glaciares por cuenca - Vista completa"""
    data = db.query(VGlaciaresAnualCuenca).all()
    return data

# ============================
# Tablas (solo campos específicos)
# ============================

@contaminantes_router.get("/coliformes-biologica", response_model=List[ColiformesBiologicaSchema])
async def get_coliformes_biologica(db: Session = Depends(get_db)):
    """Coliformes fecales en matriz biológica por estación POAL y fecha"""
    data = db.query(
        ColiformesFecalesEnMatrizBiologica.dia,
        ColiformesFecalesEnMatrizBiologica.estaciones_poal,
        ColiformesFecalesEnMatrizBiologica.value
    ).all()
    return [{"dia": row[0], "estaciones_poal": row[1], "value": row[2]} for row in data]

@contaminantes_router.get("/coliformes-acuosa", response_model=List[ColiformesAcuosaSchema])
async def get_coliformes_acuosa(db: Session = Depends(get_db)):
    """Coliformes fecales en matriz acuosa por estación POAL y fecha"""
    data = db.query(
        ColiformesFecalesEnMatrizAcuosa.dia,
        ColiformesFecalesEnMatrizAcuosa.estaciones_poal,
        ColiformesFecalesEnMatrizAcuosa.value
    ).all()
    return [{"dia": row[0], "estaciones_poal": row[1], "value": row[2]} for row in data]

@contaminantes_router.get("/metales-sedimentaria", response_model=List[MetalesSedimentariaSchema])
async def get_metales_sedimentaria(db: Session = Depends(get_db)):
    """Metales totales en matriz sedimentaria por tipo de metal y estación"""
    data = db.query(
        MetalesTotalesEnLaMatrizSedimentaria.dia,
        MetalesTotalesEnLaMatrizSedimentaria.estaciones_poal,
        MetalesTotalesEnLaMatrizSedimentaria.parametros_poal,
        MetalesTotalesEnLaMatrizSedimentaria.value
    ).all()
    return [{"dia": row[0], "estaciones_poal": row[1], "parametros_poal": row[2], "value": row[3]} for row in data]

@contaminantes_router.get("/metales-acuosa", response_model=List[MetalesAcuosaSchema])
async def get_metales_acuosa(db: Session = Depends(get_db)):
    """Metales disueltos en matriz acuosa por tipo de metal y estación"""
    data = db.query(
        MetalesDisueltosEnLaMatrizAcuosa.dia,
        MetalesDisueltosEnLaMatrizAcuosa.estaciones_poal,
        MetalesDisueltosEnLaMatrizAcuosa.parametros_poal,
        MetalesDisueltosEnLaMatrizAcuosa.value
    ).all()
    return [{"dia": row[0], "estaciones_poal": row[1], "parametros_poal": row[2], "value": row[3]} for row in data]

@hidrologia_router.get("/caudal", response_model=List[CaudalSchema])
async def get_caudal(db: Session = Depends(get_db)):
    """Caudal medio mensual de aguas corrientes por estación fluviométrica"""
    data = db.query(
        CaudalMedioDeAguasCorrientes.mes,
        CaudalMedioDeAguasCorrientes.aguas_corrientes,
        CaudalMedioDeAguasCorrientes.estaciones_fluviometricas,
        CaudalMedioDeAguasCorrientes.value
    ).all()
    return [{"mes": row[0], "aguas_corrientes": row[1], "estaciones_fluviometricas": row[2], "value": row[3]} for row in data]

@hidrologia_router.get("/pozos", response_model=List[PozoSchema])
async def get_pozos(db: Session = Depends(get_db)):
    """Nivel estático de aguas subterráneas por estación de pozo"""
    data = db.query(
        NivelEstaticoDeAguasSubterraneas.dia,
        NivelEstaticoDeAguasSubterraneas.estaciones_pozo,
        NivelEstaticoDeAguasSubterraneas.value
    ).all()
    return [{"dia": row[0], "estaciones_pozo": row[1], "value": row[2]} for row in data]

@meteorologicos_router.get("/lluvia", response_model=List[LluviaSchema])
async def get_lluvia(db: Session = Depends(get_db)):
    """Precipitación mensual por estación meteorológica DMC"""
    data = db.query(
        CantidadDeAguaCaida.mes,
        CantidadDeAguaCaida.estaciones_meteorologicas_dmc,
        CantidadDeAguaCaida.value
    ).all()
    return [{"mes": row[0], "estaciones_meteorologicas_dmc": row[1], "value": row[2]} for row in data]

@meteorologicos_router.get("/evaporacion", response_model=List[EvaporacionSchema])
async def get_evaporacion(db: Session = Depends(get_db)):
    """Evaporación real mensual por estación meteorológica"""
    data = db.query(
        EvaporacionRealPorEstacion.mes,
        EvaporacionRealPorEstacion.estacion,
        EvaporacionRealPorEstacion.value
    ).all()
    return [{"mes": row[0], "estacion": row[1], "value": row[2]} for row in data]

@meteorologicos_router.get("/nieve", response_model=List[NieveSchema])
async def get_nieve(db: Session = Depends(get_db)):
    """Altura de nieve equivalente en agua por estación nivométrica"""
    data = db.query(
        AlturaNieveEquivalenteEnAgua.dia,
        AlturaNieveEquivalenteEnAgua.estaciones_nivometricas,
        AlturaNieveEquivalenteEnAgua.value
    ).all()
    return [{"dia": row[0], "estaciones_nivometricas": row[1], "value": row[2]} for row in data]

@almacenamiento_router.get("/embalses", response_model=List[EmbalseSchema])
async def get_embalses(db: Session = Depends(get_db)):
    """Volumen mensual almacenado por embalse en todo Chile"""
    data = db.query(
        VolumenDelEmbalsePorEmbalse.mes,
        VolumenDelEmbalsePorEmbalse.embalse,
        VolumenDelEmbalsePorEmbalse.value
    ).all()
    return [{"mes": row[0], "embalse": row[1], "value": row[2]} for row in data]

# Incluir sub-routers en el router principal
router.include_router(vistas_router)
router.include_router(contaminantes_router)
router.include_router(hidrologia_router)
router.include_router(meteorologicos_router)
router.include_router(almacenamiento_router)