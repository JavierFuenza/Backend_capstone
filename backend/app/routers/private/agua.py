from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from core.dependencies import get_db
from models.agua import *
from schemas.agua import *

router = APIRouter(
    prefix="/agua",
    tags=["Agua"],
    responses={404: {"description": "No encontrado"}}
)

# ============================
# Vistas (devuelven toda la tabla)
# ============================

@router.get("/mar-mensual", response_model=List[MarMensualSchema])
async def get_mar_mensual(db: Session = Depends(get_db)):
    """Obtener todos los datos mensuales del mar"""
    data = db.query(VMarMensual).all()
    return data

@router.get("/glaciares-anual-cuenca", response_model=List[GlaciaresAnualCuencaSchema])
async def get_glaciares_anual_cuenca(db: Session = Depends(get_db)):
    """Obtener todos los datos anuales de glaciares por cuenca"""
    data = db.query(VGlaciaresAnualCuenca).all()
    return data

# ============================
# Tablas (solo campos específicos)
# ============================

@router.get("/coliformes-biologica", response_model=List[ColiformesBiologicaSchema])
async def get_coliformes_biologica(db: Session = Depends(get_db)):
    """Obtener coliformes fecales en matriz biológica - solo campos esenciales"""
    data = db.query(
        ColiformesFecalesEnMatrizBiologica.dia,
        ColiformesFecalesEnMatrizBiologica.estaciones_poal,
        ColiformesFecalesEnMatrizBiologica.value
    ).all()
    return [{"dia": row[0], "estaciones_poal": row[1], "value": row[2]} for row in data]

@router.get("/coliformes-acuosa", response_model=List[ColiformesAcuosaSchema])
async def get_coliformes_acuosa(db: Session = Depends(get_db)):
    """Obtener coliformes fecales en matriz acuosa - solo campos esenciales"""
    data = db.query(
        ColiformesFecalesEnMatrizAcuosa.dia,
        ColiformesFecalesEnMatrizAcuosa.estaciones_poal,
        ColiformesFecalesEnMatrizAcuosa.value
    ).all()
    return [{"dia": row[0], "estaciones_poal": row[1], "value": row[2]} for row in data]

@router.get("/metales-sedimentaria", response_model=List[MetalesSedimentariaSchema])
async def get_metales_sedimentaria(db: Session = Depends(get_db)):
    """Obtener metales totales en matriz sedimentaria - solo campos esenciales"""
    data = db.query(
        MetalesTotalesEnLaMatrizSedimentaria.dia,
        MetalesTotalesEnLaMatrizSedimentaria.estaciones_poal,
        MetalesTotalesEnLaMatrizSedimentaria.parametros_poal,
        MetalesTotalesEnLaMatrizSedimentaria.value
    ).all()
    return [{"dia": row[0], "estaciones_poal": row[1], "parametros_poal": row[2], "value": row[3]} for row in data]

@router.get("/metales-acuosa", response_model=List[MetalesAcuosaSchema])
async def get_metales_acuosa(db: Session = Depends(get_db)):
    """Obtener metales disueltos en matriz acuosa - solo campos esenciales"""
    data = db.query(
        MetalesDisueltosEnLaMatrizAcuosa.dia,
        MetalesDisueltosEnLaMatrizAcuosa.estaciones_poal,
        MetalesDisueltosEnLaMatrizAcuosa.parametros_poal,
        MetalesDisueltosEnLaMatrizAcuosa.value
    ).all()
    return [{"dia": row[0], "estaciones_poal": row[1], "parametros_poal": row[2], "value": row[3]} for row in data]

@router.get("/caudal", response_model=List[CaudalSchema])
async def get_caudal(db: Session = Depends(get_db)):
    """Obtener caudal medio de aguas corrientes - solo campos esenciales"""
    data = db.query(
        CaudalMedioDeAguasCorrientes.mes,
        CaudalMedioDeAguasCorrientes.aguas_corrientes,
        CaudalMedioDeAguasCorrientes.estaciones_fluviometricas,
        CaudalMedioDeAguasCorrientes.value
    ).all()
    return [{"mes": row[0], "aguas_corrientes": row[1], "estaciones_fluviometricas": row[2], "value": row[3]} for row in data]

@router.get("/lluvia", response_model=List[LluviaSchema])
async def get_lluvia(db: Session = Depends(get_db)):
    """Obtener cantidad de agua caída - solo campos esenciales"""
    data = db.query(
        CantidadDeAguaCaida.mes,
        CantidadDeAguaCaida.estaciones_meteorologicas_dmc,
        CantidadDeAguaCaida.value
    ).all()
    return [{"mes": row[0], "estaciones_meteorologicas_dmc": row[1], "value": row[2]} for row in data]

@router.get("/evaporacion", response_model=List[EvaporacionSchema])
async def get_evaporacion(db: Session = Depends(get_db)):
    """Obtener evaporación real por estación - solo campos esenciales"""
    data = db.query(
        EvaporacionRealPorEstacion.mes,
        EvaporacionRealPorEstacion.estacion,
        EvaporacionRealPorEstacion.value
    ).all()
    return [{"mes": row[0], "estacion": row[1], "value": row[2]} for row in data]

@router.get("/embalses", response_model=List[EmbalseSchema])
async def get_embalses(db: Session = Depends(get_db)):
    """Obtener volumen del embalse por embalse - solo campos esenciales"""
    data = db.query(
        VolumenDelEmbalsePorEmbalse.mes,
        VolumenDelEmbalsePorEmbalse.embalse,
        VolumenDelEmbalsePorEmbalse.value
    ).all()
    return [{"mes": row[0], "embalse": row[1], "value": row[2]} for row in data]

@router.get("/nieve", response_model=List[NieveSchema])
async def get_nieve(db: Session = Depends(get_db)):
    """Obtener altura nieve equivalente en agua - solo campos esenciales"""
    data = db.query(
        AlturaNieveEquivalenteEnAgua.dia,
        AlturaNieveEquivalenteEnAgua.estaciones_nivometricas,
        AlturaNieveEquivalenteEnAgua.value
    ).all()
    return [{"dia": row[0], "estaciones_nivometricas": row[1], "value": row[2]} for row in data]

@router.get("/pozos", response_model=List[PozoSchema])
async def get_pozos(db: Session = Depends(get_db)):
    """Obtener nivel estático de aguas subterráneas - solo campos esenciales"""
    data = db.query(
        NivelEstaticoDeAguasSubterraneas.dia,
        NivelEstaticoDeAguasSubterraneas.estaciones_pozo,
        NivelEstaticoDeAguasSubterraneas.value
    ).all()
    return [{"dia": row[0], "estaciones_pozo": row[1], "value": row[2]} for row in data]