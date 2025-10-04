from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.dependencies import get_db
from models.aire import (
    VTemperatura, VHumedadRadiacionUV, VNumEventosDeOlasDeCalor,
    VMp25Anual, VMp25Mensual, VMp10Anual, VMp10Mensual,
    VO3Anual, VO3Mensual, VSo2Anual, VSo2Mensual,
    VNo2Anual, VNo2Mensual, VCoAnual, VCoMensual
)
from schemas.metricas import (
    TemperaturaData, HumedadRadiacionUVData, OlasDeCalorData,
    ContaminanteAnualData, ContaminanteMensualData, MetricaResponse
)

router = APIRouter(
    prefix="/metricas",
    tags=["Métricas"],
    responses={404: {"description": "No encontrado"}}
)

@router.get("/temperatura/{nombre_estacion}", response_model=List[TemperaturaData])
async def get_temperatura(nombre_estacion: str, db: Session = Depends(get_db)):
    """Obtener datos de temperatura para una estación específica"""
    datos = db.query(VTemperatura).filter(
        VTemperatura.estacion == nombre_estacion
    ).all()

    if not datos:
        return []

    return datos

@router.get("/mp25/{nombre_estacion}")
async def get_mp25(nombre_estacion: str, db: Session = Depends(get_db)):
    """Obtener datos de MP2.5 (anuales y mensuales) para una estación"""
    anuales = db.query(VMp25Anual).filter(
        VMp25Anual.estacion == nombre_estacion
    ).all()

    mensuales = db.query(VMp25Mensual).filter(
        VMp25Mensual.estacion == nombre_estacion
    ).all()

    # Convertir a formato común
    datos_anuales = [{
        "anio": d.anio,
        "estacion": d.estacion,
        "max_hor_anual": d.mp25_max_hor_anual,
        "min_hor_anual": d.mp25_min_hor_anual,
        "perc50": d.mp25_perc50,
        "perc90": d.mp25_perc90,
        "perc95": d.mp25_perc95,
        "perc98": float(d.mp25_perc98) if d.mp25_perc98 else None,
        "perc99": None
    } for d in anuales]

    datos_mensuales = [{
        "mes": d.mes,
        "estacion": d.estacion,
        "med_mens": float(d.mp25_med_mens) if d.mp25_med_mens else None
    } for d in mensuales]

    return {
        "metrica": "mp25",
        "estacion": nombre_estacion,
        "tiene_datos": len(anuales) > 0 or len(mensuales) > 0,
        "datos_anuales": datos_anuales,
        "datos_mensuales": datos_mensuales
    }

@router.get("/mp10/{nombre_estacion}")
async def get_mp10(nombre_estacion: str, db: Session = Depends(get_db)):
    """Obtener datos de MP10 (anuales y mensuales) para una estación"""
    anuales = db.query(VMp10Anual).filter(
        VMp10Anual.estacion == nombre_estacion
    ).all()

    mensuales = db.query(VMp10Mensual).filter(
        VMp10Mensual.estacion == nombre_estacion
    ).all()

    datos_anuales = [{
        "anio": d.anio,
        "estacion": d.estacion,
        "max_hor_anual": d.mp10_max_hor_anual,
        "min_hor_anual": d.mp10_min_hor_anual,
        "perc50": d.mp10_perc50,
        "perc90": d.mp10_perc90,
        "perc95": d.mp10_perc95,
        "perc98": float(d.mp10_perc98) if d.mp10_perc98 else None,
        "perc99": None
    } for d in anuales]

    datos_mensuales = [{
        "mes": d.mes,
        "estacion": d.estacion,
        "med_mens": float(d.mp10_med_mens) if d.mp10_med_mens else None
    } for d in mensuales]

    return {
        "metrica": "mp10",
        "estacion": nombre_estacion,
        "tiene_datos": len(anuales) > 0 or len(mensuales) > 0,
        "datos_anuales": datos_anuales,
        "datos_mensuales": datos_mensuales
    }

@router.get("/o3/{nombre_estacion}")
async def get_o3(nombre_estacion: str, db: Session = Depends(get_db)):
    """Obtener datos de Ozono (anuales y mensuales) para una estación"""
    anuales = db.query(VO3Anual).filter(
        VO3Anual.estacion == nombre_estacion
    ).all()

    mensuales = db.query(VO3Mensual).filter(
        VO3Mensual.estacion == nombre_estacion
    ).all()

    datos_anuales = [{
        "anio": d.anio,
        "estacion": d.estacion,
        "max_hor_anual": d.o3_max_hor_anual,
        "min_hor_anual": d.o3_min_hor_anual,
        "perc50": d.o3_perc50,
        "perc90": d.o3_perc90,
        "perc95": d.o3_perc95,
        "perc98": d.o3_perc98,
        "perc99": d.o3_perc99
    } for d in anuales]

    datos_mensuales = [{
        "mes": d.mes,
        "estacion": d.estacion,
        "med_mens": d.o3_med_mens
    } for d in mensuales]

    return {
        "metrica": "o3",
        "estacion": nombre_estacion,
        "tiene_datos": len(anuales) > 0 or len(mensuales) > 0,
        "datos_anuales": datos_anuales,
        "datos_mensuales": datos_mensuales
    }

@router.get("/so2/{nombre_estacion}")
async def get_so2(nombre_estacion: str, db: Session = Depends(get_db)):
    """Obtener datos de SO2 (anuales y mensuales) para una estación"""
    anuales = db.query(VSo2Anual).filter(
        VSo2Anual.estacion == nombre_estacion
    ).all()

    mensuales = db.query(VSo2Mensual).filter(
        VSo2Mensual.estacion == nombre_estacion
    ).all()

    datos_anuales = [{
        "anio": d.anio,
        "estacion": d.estacion,
        "max_hor_anual": d.so2_max_hor_anual,
        "min_hor_anual": d.so2_min_anual,
        "perc50": d.so2_perc50,
        "perc90": d.so2_perc90,
        "perc95": d.so2_perc95,
        "perc98": d.so2_perc98,
        "perc99": d.so2_perc99
    } for d in anuales]

    datos_mensuales = [{
        "mes": d.mes,
        "estacion": d.estacion,
        "med_mens": d.so2_med_mens
    } for d in mensuales]

    return {
        "metrica": "so2",
        "estacion": nombre_estacion,
        "tiene_datos": len(anuales) > 0 or len(mensuales) > 0,
        "datos_anuales": datos_anuales,
        "datos_mensuales": datos_mensuales
    }

@router.get("/no2/{nombre_estacion}")
async def get_no2(nombre_estacion: str, db: Session = Depends(get_db)):
    """Obtener datos de NO2 (anuales y mensuales) para una estación"""
    anuales = db.query(VNo2Anual).filter(
        VNo2Anual.estacion == nombre_estacion
    ).all()

    mensuales = db.query(VNo2Mensual).filter(
        VNo2Mensual.estacion == nombre_estacion
    ).all()

    datos_anuales = [{
        "anio": d.anio,
        "estacion": d.estacion,
        "max_hor_anual": d.no2_max_hor_anual,
        "min_hor_anual": d.no2_min_hor_anual,
        "perc50": d.no2_perc50,
        "perc90": d.no2_perc90,
        "perc95": d.no2_perc95,
        "perc98": d.no2_perc98,
        "perc99": d.no2_perc99
    } for d in anuales]

    datos_mensuales = [{
        "mes": d.mes,
        "estacion": d.estacion,
        "med_mens": d.no2_med_mens
    } for d in mensuales]

    return {
        "metrica": "no2",
        "estacion": nombre_estacion,
        "tiene_datos": len(anuales) > 0 or len(mensuales) > 0,
        "datos_anuales": datos_anuales,
        "datos_mensuales": datos_mensuales
    }

@router.get("/co/{nombre_estacion}")
async def get_co(nombre_estacion: str, db: Session = Depends(get_db)):
    """Obtener datos de CO (anuales y mensuales) para una estación"""
    anuales = db.query(VCoAnual).filter(
        VCoAnual.estacion == nombre_estacion
    ).all()

    mensuales = db.query(VCoMensual).filter(
        VCoMensual.estacion == nombre_estacion
    ).all()

    datos_anuales = [{
        "anio": d.anio,
        "estacion": d.estacion,
        "max_hor_anual": d.co_max_hor_anual,
        "min_hor_anual": d.co_min_hor_anual,
        "perc50": d.co_perc50,
        "perc90": d.co_perc90,
        "perc95": d.co_perc95,
        "perc98": d.co_perc98,
        "perc99": d.co_perc99
    } for d in anuales]

    datos_mensuales = [{
        "mes": d.mes,
        "estacion": d.estacion,
        "med_mens": d.co_med_mens
    } for d in mensuales]

    return {
        "metrica": "co",
        "estacion": nombre_estacion,
        "tiene_datos": len(anuales) > 0 or len(mensuales) > 0,
        "datos_anuales": datos_anuales,
        "datos_mensuales": datos_mensuales
    }

@router.get("/otros/{nombre_estacion}")
async def get_otros(nombre_estacion: str, db: Session = Depends(get_db)):
    """Obtener datos de Humedad, Radiación UV y Olas de Calor para una estación"""
    humedad_rad_uv = db.query(VHumedadRadiacionUV).filter(
        VHumedadRadiacionUV.estacion == nombre_estacion
    ).all()

    olas_calor = db.query(VNumEventosDeOlasDeCalor).filter(
        VNumEventosDeOlasDeCalor.estacion == nombre_estacion
    ).all()

    return {
        "estacion": nombre_estacion,
        "humedad_radiacion_uv": [
            {
                "mes": d.mes,
                "humedad_rel_med_mens": d.humedad_rel_med_mens,
                "rad_global_med": d.rad_global_med,
                "uvb_prom": d.uvb_prom
            } for d in humedad_rad_uv
        ],
        "olas_de_calor": [
            {
                "mes": d.mes,
                "num_eventos": d.num_eventos_de_olas_de_calor
            } for d in olas_calor
        ],
        "tiene_datos": len(humedad_rad_uv) > 0 or len(olas_calor) > 0
    }
