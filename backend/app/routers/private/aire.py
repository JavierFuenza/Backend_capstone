from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.dependencies import get_db
from models.aire import *
from schemas.aire import *

router = APIRouter(
    prefix="/aire",
    tags=["Aire"],
    responses={404: {"description": "No encontrado"}}
)

@router.get("/temperatura", response_model=List[TemperaturaSchema])
async def get_temperatura(db: Session = Depends(get_db)):
    """Obtener todos los datos de temperatura"""
    data = db.query(VTemperatura).all()
    return data

@router.get("/humedad-radiacion-uv", response_model=List[HumedadRadiacionUVSchema])
async def get_humedad_radiacion_uv(db: Session = Depends(get_db)):
    """Obtener todos los datos de humedad, radiación y UV"""
    data = db.query(VHumedadRadiacionUV).all()
    return data

@router.get("/mp25/anual", response_model=List[Mp25AnualSchema])
async def get_mp25_anual(db: Session = Depends(get_db)):
    """Obtener todos los datos anuales de MP2.5"""
    data = db.query(VMp25Anual).all()
    return data

@router.get("/mp25/mensual", response_model=List[Mp25MensualSchema])
async def get_mp25_mensual(db: Session = Depends(get_db)):
    """Obtener todos los datos mensuales de MP2.5"""
    data = db.query(VMp25Mensual).all()
    return data

@router.get("/mp10/anual", response_model=List[Mp10AnualSchema])
async def get_mp10_anual(db: Session = Depends(get_db)):
    """Obtener todos los datos anuales de MP10"""
    data = db.query(VMp10Anual).all()
    return data

@router.get("/mp10/mensual", response_model=List[Mp10MensualSchema])
async def get_mp10_mensual(db: Session = Depends(get_db)):
    """Obtener todos los datos mensuales de MP10"""
    data = db.query(VMp10Mensual).all()
    return data

@router.get("/o3/anual", response_model=List[O3AnualSchema])
async def get_o3_anual(db: Session = Depends(get_db)):
    """Obtener todos los datos anuales de Ozono (O3)"""
    data = db.query(VO3Anual).all()
    return data

@router.get("/o3/mensual", response_model=List[O3MensualSchema])
async def get_o3_mensual(db: Session = Depends(get_db)):
    """Obtener todos los datos mensuales de Ozono (O3)"""
    data = db.query(VO3Mensual).all()
    return data

@router.get("/so2/anual", response_model=List[So2AnualSchema])
async def get_so2_anual(db: Session = Depends(get_db)):
    """Obtener todos los datos anuales de Dióxido de Azufre (SO2)"""
    data = db.query(VSo2Anual).all()
    return data

@router.get("/so2/mensual", response_model=List[So2MensualSchema])
async def get_so2_mensual(db: Session = Depends(get_db)):
    """Obtener todos los datos mensuales de Dióxido de Azufre (SO2)"""
    data = db.query(VSo2Mensual).all()
    return data

@router.get("/no2/anual", response_model=List[No2AnualSchema])
async def get_no2_anual(db: Session = Depends(get_db)):
    """Obtener todos los datos anuales de Dióxido de Nitrógeno (NO2)"""
    data = db.query(VNo2Anual).all()
    return data

@router.get("/no2/mensual", response_model=List[No2MensualSchema])
async def get_no2_mensual(db: Session = Depends(get_db)):
    """Obtener todos los datos mensuales de Dióxido de Nitrógeno (NO2)"""
    data = db.query(VNo2Mensual).all()
    return data

@router.get("/co/anual", response_model=List[CoAnualSchema])
async def get_co_anual(db: Session = Depends(get_db)):
    """Obtener todos los datos anuales de Monóxido de Carbono (CO)"""
    data = db.query(VCoAnual).all()
    return data

@router.get("/co/mensual", response_model=List[CoMensualSchema])
async def get_co_mensual(db: Session = Depends(get_db)):
    """Obtener todos los datos mensuales de Monóxido de Carbono (CO)"""
    data = db.query(VCoMensual).all()
    return data

@router.get("/no/anual", response_model=List[NoAnualSchema])
async def get_no_anual(db: Session = Depends(get_db)):
    """Obtener todos los datos anuales de Óxido de Nitrógeno (NO)"""
    data = db.query(VNoAnual).all()
    return data

@router.get("/no/mensual", response_model=List[NoMensualSchema])
async def get_no_mensual(db: Session = Depends(get_db)):
    """Obtener todos los datos mensuales de Óxido de Nitrógeno (NO)"""
    data = db.query(VNoMensual).all()
    return data

@router.get("/nox/anual", response_model=List[NoxAnualSchema])
async def get_nox_anual(db: Session = Depends(get_db)):
    """Obtener todos los datos anuales de Óxidos de Nitrógeno (NOx)"""
    data = db.query(VNoxAnual).all()
    return data

@router.get("/nox/mensual", response_model=List[NoxMensualSchema])
async def get_nox_mensual(db: Session = Depends(get_db)):
    """Obtener todos los datos mensuales de Óxidos de Nitrógeno (NOx)"""
    data = db.query(VNoxMensual).all()
    return data

@router.get("/olas-calor", response_model=List[OlasCalorSchema])
async def get_olas_calor(db: Session = Depends(get_db)):
    """Obtener todos los datos de eventos de olas de calor"""
    data = db.query(VNumEventosDeOlasDeCalor).all()
    return data