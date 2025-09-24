from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.dependencies import get_db
from models.aire import *
from schemas.aire import *

# Crear sub-routers para organizar endpoints
general_router = APIRouter(
    prefix="/aire/climaticos",
    tags=["Aire - Climáticos"],
    responses={404: {"description": "No encontrado"}}
)

mp25_router = APIRouter(
    prefix="/aire/mp25",
    tags=["Aire - MP2.5"],
    responses={404: {"description": "No encontrado"}}
)

mp10_router = APIRouter(
    prefix="/aire/mp10",
    tags=["Aire - MP10"],
    responses={404: {"description": "No encontrado"}}
)

o3_router = APIRouter(
    prefix="/aire/o3",
    tags=["Aire - Ozono (O3)"],
    responses={404: {"description": "No encontrado"}}
)

so2_router = APIRouter(
    prefix="/aire/so2",
    tags=["Aire - Dióxido de Azufre (SO2)"],
    responses={404: {"description": "No encontrado"}}
)

no2_router = APIRouter(
    prefix="/aire/no2",
    tags=["Aire - Dióxido de Nitrógeno (NO2)"],
    responses={404: {"description": "No encontrado"}}
)

co_router = APIRouter(
    prefix="/aire/co",
    tags=["Aire - Monóxido de Carbono (CO)"],
    responses={404: {"description": "No encontrado"}}
)

no_router = APIRouter(
    prefix="/aire/no",
    tags=["Aire - Óxido de Nitrógeno (NO)"],
    responses={404: {"description": "No encontrado"}}
)

nox_router = APIRouter(
    prefix="/aire/nox",
    tags=["Aire - Óxidos de Nitrógeno (NOx)"],
    responses={404: {"description": "No encontrado"}}
)

eventos_router = APIRouter(
    prefix="/aire/eventos",
    tags=["Aire - Eventos Climáticos"],
    responses={404: {"description": "No encontrado"}}
)

# Router principal para incluir en main.py
router = APIRouter()

@general_router.get("/temperatura", response_model=List[TemperaturaSchema])
async def get_temperatura(db: Session = Depends(get_db)):
    """Obtener todos los datos de temperatura por estación y mes"""
    data = db.query(VTemperatura).all()
    return data

@general_router.get("/humedad-radiacion-uv", response_model=List[HumedadRadiacionUVSchema])
async def get_humedad_radiacion_uv(db: Session = Depends(get_db)):
    """Obtener datos de humedad relativa, radiación global y radiación UVB"""
    data = db.query(VHumedadRadiacionUV).all()
    return data

@mp25_router.get("/anual", response_model=List[Mp25AnualSchema])
async def get_mp25_anual(db: Session = Depends(get_db)):
    """Datos anuales de Material Particulado 2.5 - estadísticas por estación"""
    data = db.query(VMp25Anual).all()
    return data

@mp25_router.get("/mensual", response_model=List[Mp25MensualSchema])
async def get_mp25_mensual(db: Session = Depends(get_db)):
    """Datos mensuales de Material Particulado 2.5 - promedio por estación"""
    data = db.query(VMp25Mensual).all()
    return data

@mp10_router.get("/anual", response_model=List[Mp10AnualSchema])
async def get_mp10_anual(db: Session = Depends(get_db)):
    """Datos anuales de Material Particulado 10 - estadísticas por estación"""
    data = db.query(VMp10Anual).all()
    return data

@mp10_router.get("/mensual", response_model=List[Mp10MensualSchema])
async def get_mp10_mensual(db: Session = Depends(get_db)):
    """Datos mensuales de Material Particulado 10 - promedio por estación"""
    data = db.query(VMp10Mensual).all()
    return data

@o3_router.get("/anual", response_model=List[O3AnualSchema])
async def get_o3_anual(db: Session = Depends(get_db)):
    """Datos anuales de Ozono troposférico - estadísticas por estación"""
    data = db.query(VO3Anual).all()
    return data

@o3_router.get("/mensual", response_model=List[O3MensualSchema])
async def get_o3_mensual(db: Session = Depends(get_db)):
    """Datos mensuales de Ozono troposférico - promedio por estación"""
    data = db.query(VO3Mensual).all()
    return data

@so2_router.get("/anual", response_model=List[So2AnualSchema])
async def get_so2_anual(db: Session = Depends(get_db)):
    """Datos anuales de SO2 - estadísticas por estación de monitoreo"""
    data = db.query(VSo2Anual).all()
    return data

@so2_router.get("/mensual", response_model=List[So2MensualSchema])
async def get_so2_mensual(db: Session = Depends(get_db)):
    """Datos mensuales de SO2 - promedio por estación de monitoreo"""
    data = db.query(VSo2Mensual).all()
    return data

@no2_router.get("/anual", response_model=List[No2AnualSchema])
async def get_no2_anual(db: Session = Depends(get_db)):
    """Datos anuales de NO2 - estadísticas por estación de monitoreo"""
    data = db.query(VNo2Anual).all()
    return data

@no2_router.get("/mensual", response_model=List[No2MensualSchema])
async def get_no2_mensual(db: Session = Depends(get_db)):
    """Datos mensuales de NO2 - promedio por estación de monitoreo"""
    data = db.query(VNo2Mensual).all()
    return data

@co_router.get("/anual", response_model=List[CoAnualSchema])
async def get_co_anual(db: Session = Depends(get_db)):
    """Datos anuales de CO - estadísticas por estación de monitoreo"""
    data = db.query(VCoAnual).all()
    return data

@co_router.get("/mensual", response_model=List[CoMensualSchema])
async def get_co_mensual(db: Session = Depends(get_db)):
    """Datos mensuales de CO - promedio por estación de monitoreo"""
    data = db.query(VCoMensual).all()
    return data

@no_router.get("/anual", response_model=List[NoAnualSchema])
async def get_no_anual(db: Session = Depends(get_db)):
    """Datos anuales de NO - estadísticas por estación de monitoreo"""
    data = db.query(VNoAnual).all()
    return data

@no_router.get("/mensual", response_model=List[NoMensualSchema])
async def get_no_mensual(db: Session = Depends(get_db)):
    """Datos mensuales de NO - promedio por estación de monitoreo"""
    data = db.query(VNoMensual).all()
    return data

@nox_router.get("/anual", response_model=List[NoxAnualSchema])
async def get_nox_anual(db: Session = Depends(get_db)):
    """Datos anuales de NOx - estadísticas por estación de monitoreo"""
    data = db.query(VNoxAnual).all()
    return data

@nox_router.get("/mensual", response_model=List[NoxMensualSchema])
async def get_nox_mensual(db: Session = Depends(get_db)):
    """Datos mensuales de NOx - promedio por estación de monitoreo"""
    data = db.query(VNoxMensual).all()
    return data

@eventos_router.get("/olas-calor", response_model=List[OlasCalorSchema])
async def get_olas_calor(db: Session = Depends(get_db)):
    """Número de eventos de olas de calor por región y año"""
    data = db.query(VNumEventosDeOlasDeCalor).all()
    return data

# Incluir sub-routers en el router principal
router.include_router(general_router)
router.include_router(mp25_router)
router.include_router(mp10_router)
router.include_router(o3_router)
router.include_router(so2_router)
router.include_router(no2_router)
router.include_router(co_router)
router.include_router(no_router)
router.include_router(nox_router)
router.include_router(eventos_router)