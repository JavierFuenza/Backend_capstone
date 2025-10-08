from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import distinct
from typing import List, Optional

from core.dependencies import get_db
from models.estaciones import Estacion
from models.aire import (
    VTemperatura, VHumedadRadiacionUV, VNumEventosDeOlasDeCalor,
    VMp25Anual, VMp25Mensual, VMp10Anual, VMp10Mensual,
    VO3Anual, VO3Mensual, VSo2Anual, VSo2Mensual,
    VNo2Anual, VNo2Mensual, VCoAnual, VCoMensual,
    VNoAnual, VNoMensual, VNoxAnual, VNoxMensual
)
from schemas.estaciones import EstacionSchema, RegionSchema, EstacionMetricasSchema, EstacionSubmetricasSchema

router = APIRouter(
    prefix="/estaciones",
    tags=["Estaciones"],
    responses={404: {"description": "No encontrado"}}
)

@router.get("/metricas", response_model=EstacionMetricasSchema)
async def get_estacion_metricas(
    db: Session = Depends(get_db),
    estacion_id: Optional[int] = Query(None, description="ID de la estación"),
    nombre: Optional[str] = Query(None, description="Nombre de la estación")
):
    """Obtener métricas disponibles para una estación específica (por ID o nombre)"""

    # Validar que se proporcione al menos un parámetro
    if not estacion_id and not nombre:
        raise HTTPException(
            status_code=400,
            detail="Debe proporcionar 'estacion_id' o 'nombre'"
        )

    # Buscar la estación
    query = db.query(Estacion)
    if estacion_id:
        query = query.filter(Estacion.id == estacion_id)
    else:
        query = query.filter(Estacion.nombre == nombre)

    estacion = query.first()
    if not estacion:
        raise HTTPException(
            status_code=404,
            detail=f"Estación no encontrada"
        )

    # Verificar qué métricas tiene disponibles
    metricas = []

    # Verificar Temperatura
    tiene_temperatura = db.query(VTemperatura).filter(
        VTemperatura.estacion == estacion.nombre
    ).first() is not None
    if tiene_temperatura:
        metricas.append("Temperatura")

    # Verificar Humedad, Radiación y UV
    tiene_humedad_radiacion_uv = db.query(VHumedadRadiacionUV).filter(
        VHumedadRadiacionUV.estacion == estacion.nombre
    ).first() is not None
    if tiene_humedad_radiacion_uv:
        metricas.append("Humedad Radiación y UV")

    # Verificar Contaminantes (MP2.5, MP10, O3, SO2, NO2, CO, NO, NOX)
    tiene_contaminantes = any([
        db.query(VMp25Anual).filter(VMp25Anual.estacion == estacion.nombre).first() is not None,
        db.query(VMp25Mensual).filter(VMp25Mensual.estacion == estacion.nombre).first() is not None,
        db.query(VMp10Anual).filter(VMp10Anual.estacion == estacion.nombre).first() is not None,
        db.query(VMp10Mensual).filter(VMp10Mensual.estacion == estacion.nombre).first() is not None,
        db.query(VO3Anual).filter(VO3Anual.estacion == estacion.nombre).first() is not None,
        db.query(VO3Mensual).filter(VO3Mensual.estacion == estacion.nombre).first() is not None,
        db.query(VSo2Anual).filter(VSo2Anual.estacion == estacion.nombre).first() is not None,
        db.query(VSo2Mensual).filter(VSo2Mensual.estacion == estacion.nombre).first() is not None,
        db.query(VNo2Anual).filter(VNo2Anual.estacion == estacion.nombre).first() is not None,
        db.query(VNo2Mensual).filter(VNo2Mensual.estacion == estacion.nombre).first() is not None,
        db.query(VCoAnual).filter(VCoAnual.estacion == estacion.nombre).first() is not None,
        db.query(VCoMensual).filter(VCoMensual.estacion == estacion.nombre).first() is not None,
        db.query(VNoAnual).filter(VNoAnual.estacion == estacion.nombre).first() is not None,
        db.query(VNoMensual).filter(VNoMensual.estacion == estacion.nombre).first() is not None,
        db.query(VNoxAnual).filter(VNoxAnual.estacion == estacion.nombre).first() is not None,
        db.query(VNoxMensual).filter(VNoxMensual.estacion == estacion.nombre).first() is not None,
    ])
    if tiene_contaminantes:
        metricas.append("Contaminantes")

    # Verificar Eventos de Olas de Calor
    tiene_olas_calor = db.query(VNumEventosDeOlasDeCalor).filter(
        VNumEventosDeOlasDeCalor.estacion == estacion.nombre
    ).first() is not None
    if tiene_olas_calor:
        metricas.append("Eventos de Olas de Calor")

    return {
        "id": estacion.id,
        "nombre": estacion.nombre,
        "descripcion": estacion.descripcion,
        "metricas_disponibles": metricas
    }

@router.get("/submetricas", response_model=EstacionSubmetricasSchema)
async def get_estacion_submetricas(
    db: Session = Depends(get_db),
    metrica: str = Query(..., description="Categoría de métrica: Temperatura, Humedad Radiación y UV, Contaminantes, Eventos de Olas de Calor"),
    estacion_id: Optional[int] = Query(None, description="ID de la estación"),
    nombre: Optional[str] = Query(None, description="Nombre de la estación")
):
    """Obtener submmétricas específicas disponibles (columnas con >= 2 registros no nulos)"""

    # Validar que se proporcione al menos un parámetro de estación
    if not estacion_id and not nombre:
        raise HTTPException(
            status_code=400,
            detail="Debe proporcionar 'estacion_id' o 'nombre'"
        )

    # Buscar la estación
    query = db.query(Estacion)
    if estacion_id:
        query = query.filter(Estacion.id == estacion_id)
    else:
        query = query.filter(Estacion.nombre == nombre)

    estacion = query.first()
    if not estacion:
        raise HTTPException(
            status_code=404,
            detail=f"Estación no encontrada"
        )

    submetricas = []

    # ====================
    # TEMPERATURA
    # ====================
    if metrica.lower() == "temperatura":
        # Verificar cada columna de la vista v_temperatura
        if db.query(VTemperatura).filter(
            VTemperatura.estacion == estacion.nombre,
            VTemperatura.temp_max_absoluta.isnot(None)
        ).count() >= 2:
            submetricas.append("Temperatura Máxima Absoluta")

        if db.query(VTemperatura).filter(
            VTemperatura.estacion == estacion.nombre,
            VTemperatura.temp_min_absoluta.isnot(None)
        ).count() >= 2:
            submetricas.append("Temperatura Mínima Absoluta")

        if db.query(VTemperatura).filter(
            VTemperatura.estacion == estacion.nombre,
            VTemperatura.temp_max_med.isnot(None)
        ).count() >= 2:
            submetricas.append("Temperatura Máxima Media")

        if db.query(VTemperatura).filter(
            VTemperatura.estacion == estacion.nombre,
            VTemperatura.temp_min_med.isnot(None)
        ).count() >= 2:
            submetricas.append("Temperatura Mínima Media")

        if db.query(VTemperatura).filter(
            VTemperatura.estacion == estacion.nombre,
            VTemperatura.temp_med.isnot(None)
        ).count() >= 2:
            submetricas.append("Temperatura Media")

    # ====================
    # HUMEDAD, RADIACIÓN Y UV
    # ====================
    elif "humedad" in metrica.lower() or "radiación" in metrica.lower() or "radiacion" in metrica.lower():
        # Verificar cada columna de la vista v_humedad_radiacion_uv
        if db.query(VHumedadRadiacionUV).filter(
            VHumedadRadiacionUV.estacion == estacion.nombre,
            VHumedadRadiacionUV.humedad_rel_med_mens.isnot(None)
        ).count() >= 2:
            submetricas.append("Humedad Relativa Media Mensual")

        if db.query(VHumedadRadiacionUV).filter(
            VHumedadRadiacionUV.estacion == estacion.nombre,
            VHumedadRadiacionUV.rad_global_med.isnot(None)
        ).count() >= 2:
            submetricas.append("Radiación Global Media")

        if db.query(VHumedadRadiacionUV).filter(
            VHumedadRadiacionUV.estacion == estacion.nombre,
            VHumedadRadiacionUV.uvb_prom.isnot(None)
        ).count() >= 2:
            submetricas.append("UVB Promedio")

    # ====================
    # CONTAMINANTES
    # ====================
    elif metrica.lower() == "contaminantes":
        # MP2.5 Anual - Verificar cada columna
        if db.query(VMp25Anual).filter(
            VMp25Anual.estacion == estacion.nombre,
            VMp25Anual.mp25_max_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("MP2.5 - Máximo Horario Anual")

        if db.query(VMp25Anual).filter(
            VMp25Anual.estacion == estacion.nombre,
            VMp25Anual.mp25_min_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("MP2.5 - Mínimo Horario Anual")

        if db.query(VMp25Anual).filter(
            VMp25Anual.estacion == estacion.nombre,
            VMp25Anual.mp25_perc50.isnot(None)
        ).count() >= 2:
            submetricas.append("MP2.5 - Percentil 50")

        if db.query(VMp25Anual).filter(
            VMp25Anual.estacion == estacion.nombre,
            VMp25Anual.mp25_perc90.isnot(None)
        ).count() >= 2:
            submetricas.append("MP2.5 - Percentil 90")

        if db.query(VMp25Anual).filter(
            VMp25Anual.estacion == estacion.nombre,
            VMp25Anual.mp25_perc95.isnot(None)
        ).count() >= 2:
            submetricas.append("MP2.5 - Percentil 95")

        if db.query(VMp25Anual).filter(
            VMp25Anual.estacion == estacion.nombre,
            VMp25Anual.mp25_perc98.isnot(None)
        ).count() >= 2:
            submetricas.append("MP2.5 - Percentil 98")

        # MP2.5 Mensual
        if db.query(VMp25Mensual).filter(
            VMp25Mensual.estacion == estacion.nombre,
            VMp25Mensual.mp25_med_mens.isnot(None)
        ).count() >= 2:
            submetricas.append("MP2.5 - Media Mensual")

        # MP10 Anual - Verificar cada columna
        if db.query(VMp10Anual).filter(
            VMp10Anual.estacion == estacion.nombre,
            VMp10Anual.mp10_max_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("MP10 - Máximo Horario Anual")

        if db.query(VMp10Anual).filter(
            VMp10Anual.estacion == estacion.nombre,
            VMp10Anual.mp10_min_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("MP10 - Mínimo Horario Anual")

        if db.query(VMp10Anual).filter(
            VMp10Anual.estacion == estacion.nombre,
            VMp10Anual.mp10_perc50.isnot(None)
        ).count() >= 2:
            submetricas.append("MP10 - Percentil 50")

        if db.query(VMp10Anual).filter(
            VMp10Anual.estacion == estacion.nombre,
            VMp10Anual.mp10_perc90.isnot(None)
        ).count() >= 2:
            submetricas.append("MP10 - Percentil 90")

        if db.query(VMp10Anual).filter(
            VMp10Anual.estacion == estacion.nombre,
            VMp10Anual.mp10_perc95.isnot(None)
        ).count() >= 2:
            submetricas.append("MP10 - Percentil 95")

        if db.query(VMp10Anual).filter(
            VMp10Anual.estacion == estacion.nombre,
            VMp10Anual.mp10_perc98.isnot(None)
        ).count() >= 2:
            submetricas.append("MP10 - Percentil 98")

        # MP10 Mensual
        if db.query(VMp10Mensual).filter(
            VMp10Mensual.estacion == estacion.nombre,
            VMp10Mensual.mp10_med_mens.isnot(None)
        ).count() >= 2:
            submetricas.append("MP10 - Media Mensual")

        # O3 Anual
        if db.query(VO3Anual).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_max_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("O3 - Máximo Horario Anual")

        if db.query(VO3Anual).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_min_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("O3 - Mínimo Horario Anual")

        if db.query(VO3Anual).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_perc50.isnot(None)
        ).count() >= 2:
            submetricas.append("O3 - Percentil 50")

        if db.query(VO3Anual).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_perc90.isnot(None)
        ).count() >= 2:
            submetricas.append("O3 - Percentil 90")

        if db.query(VO3Anual).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_perc95.isnot(None)
        ).count() >= 2:
            submetricas.append("O3 - Percentil 95")

        if db.query(VO3Anual).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_perc98.isnot(None)
        ).count() >= 2:
            submetricas.append("O3 - Percentil 98")

        if db.query(VO3Anual).filter(
            VO3Anual.estacion == estacion.nombre,
            VO3Anual.o3_perc99.isnot(None)
        ).count() >= 2:
            submetricas.append("O3 - Percentil 99")

        # O3 Mensual
        if db.query(VO3Mensual).filter(
            VO3Mensual.estacion == estacion.nombre,
            VO3Mensual.o3_med_mens.isnot(None)
        ).count() >= 2:
            submetricas.append("O3 - Media Mensual")

        # SO2 Anual
        if db.query(VSo2Anual).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_max_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("SO2 - Máximo Horario Anual")

        if db.query(VSo2Anual).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_min_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("SO2 - Mínimo Anual")

        if db.query(VSo2Anual).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_perc50.isnot(None)
        ).count() >= 2:
            submetricas.append("SO2 - Percentil 50")

        if db.query(VSo2Anual).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_perc90.isnot(None)
        ).count() >= 2:
            submetricas.append("SO2 - Percentil 90")

        if db.query(VSo2Anual).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_perc95.isnot(None)
        ).count() >= 2:
            submetricas.append("SO2 - Percentil 95")

        if db.query(VSo2Anual).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_perc98.isnot(None)
        ).count() >= 2:
            submetricas.append("SO2 - Percentil 98")

        if db.query(VSo2Anual).filter(
            VSo2Anual.estacion == estacion.nombre,
            VSo2Anual.so2_perc99.isnot(None)
        ).count() >= 2:
            submetricas.append("SO2 - Percentil 99")

        # SO2 Mensual
        if db.query(VSo2Mensual).filter(
            VSo2Mensual.estacion == estacion.nombre,
            VSo2Mensual.so2_med_mens.isnot(None)
        ).count() >= 2:
            submetricas.append("SO2 - Media Mensual")

        # NO2 Anual
        if db.query(VNo2Anual).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_max_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("NO2 - Máximo Horario Anual")

        if db.query(VNo2Anual).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_min_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("NO2 - Mínimo Horario Anual")

        if db.query(VNo2Anual).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_perc50.isnot(None)
        ).count() >= 2:
            submetricas.append("NO2 - Percentil 50")

        if db.query(VNo2Anual).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_perc90.isnot(None)
        ).count() >= 2:
            submetricas.append("NO2 - Percentil 90")

        if db.query(VNo2Anual).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_perc95.isnot(None)
        ).count() >= 2:
            submetricas.append("NO2 - Percentil 95")

        if db.query(VNo2Anual).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_perc98.isnot(None)
        ).count() >= 2:
            submetricas.append("NO2 - Percentil 98")

        if db.query(VNo2Anual).filter(
            VNo2Anual.estacion == estacion.nombre,
            VNo2Anual.no2_perc99.isnot(None)
        ).count() >= 2:
            submetricas.append("NO2 - Percentil 99")

        # NO2 Mensual
        if db.query(VNo2Mensual).filter(
            VNo2Mensual.estacion == estacion.nombre,
            VNo2Mensual.no2_med_mens.isnot(None)
        ).count() >= 2:
            submetricas.append("NO2 - Media Mensual")

        # CO Anual
        if db.query(VCoAnual).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_max_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("CO - Máximo Horario Anual")

        if db.query(VCoAnual).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_min_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("CO - Mínimo Horario Anual")

        if db.query(VCoAnual).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_perc50.isnot(None)
        ).count() >= 2:
            submetricas.append("CO - Percentil 50")

        if db.query(VCoAnual).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_perc90.isnot(None)
        ).count() >= 2:
            submetricas.append("CO - Percentil 90")

        if db.query(VCoAnual).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_perc95.isnot(None)
        ).count() >= 2:
            submetricas.append("CO - Percentil 95")

        if db.query(VCoAnual).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_perc98.isnot(None)
        ).count() >= 2:
            submetricas.append("CO - Percentil 98")

        if db.query(VCoAnual).filter(
            VCoAnual.estacion == estacion.nombre,
            VCoAnual.co_perc99.isnot(None)
        ).count() >= 2:
            submetricas.append("CO - Percentil 99")

        # CO Mensual
        if db.query(VCoMensual).filter(
            VCoMensual.estacion == estacion.nombre,
            VCoMensual.co_med_mens.isnot(None)
        ).count() >= 2:
            submetricas.append("CO - Media Mensual")

        # NO Anual
        if db.query(VNoAnual).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_max_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("NO - Máximo Horario Anual")

        if db.query(VNoAnual).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_min_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("NO - Mínimo Horario Anual")

        if db.query(VNoAnual).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_perc50.isnot(None)
        ).count() >= 2:
            submetricas.append("NO - Percentil 50")

        if db.query(VNoAnual).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_perc90.isnot(None)
        ).count() >= 2:
            submetricas.append("NO - Percentil 90")

        if db.query(VNoAnual).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_perc95.isnot(None)
        ).count() >= 2:
            submetricas.append("NO - Percentil 95")

        if db.query(VNoAnual).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_perc98.isnot(None)
        ).count() >= 2:
            submetricas.append("NO - Percentil 98")

        if db.query(VNoAnual).filter(
            VNoAnual.estacion == estacion.nombre,
            VNoAnual.no_perc99.isnot(None)
        ).count() >= 2:
            submetricas.append("NO - Percentil 99")

        # NO Mensual
        if db.query(VNoMensual).filter(
            VNoMensual.estacion == estacion.nombre,
            VNoMensual.no_med_mens.isnot(None)
        ).count() >= 2:
            submetricas.append("NO - Media Mensual")

        # NOX Anual
        if db.query(VNoxAnual).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_max_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("NOX - Máximo Horario Anual")

        if db.query(VNoxAnual).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_min_hor_anual.isnot(None)
        ).count() >= 2:
            submetricas.append("NOX - Mínimo Horario Anual")

        if db.query(VNoxAnual).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_perc50.isnot(None)
        ).count() >= 2:
            submetricas.append("NOX - Percentil 50")

        if db.query(VNoxAnual).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_perc90.isnot(None)
        ).count() >= 2:
            submetricas.append("NOX - Percentil 90")

        if db.query(VNoxAnual).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_perc95.isnot(None)
        ).count() >= 2:
            submetricas.append("NOX - Percentil 95")

        if db.query(VNoxAnual).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_perc98.isnot(None)
        ).count() >= 2:
            submetricas.append("NOX - Percentil 98")

        if db.query(VNoxAnual).filter(
            VNoxAnual.estacion == estacion.nombre,
            VNoxAnual.nox_perc99.isnot(None)
        ).count() >= 2:
            submetricas.append("NOX - Percentil 99")

        # NOX Mensual
        if db.query(VNoxMensual).filter(
            VNoxMensual.estacion == estacion.nombre,
            VNoxMensual.nox_med_mens.isnot(None)
        ).count() >= 2:
            submetricas.append("NOX - Media Mensual")

    # ====================
    # EVENTOS DE OLAS DE CALOR
    # ====================
    elif "olas de calor" in metrica.lower() or "eventos" in metrica.lower():
        if db.query(VNumEventosDeOlasDeCalor).filter(
            VNumEventosDeOlasDeCalor.estacion == estacion.nombre,
            VNumEventosDeOlasDeCalor.num_eventos_de_olas_de_calor.isnot(None)
        ).count() >= 2:
            submetricas.append("Número de Eventos de Olas de Calor")

    else:
        raise HTTPException(
            status_code=400,
            detail=f"Métrica '{metrica}' no válida. Use: Temperatura, Humedad Radiación y UV, Contaminantes, o Eventos de Olas de Calor"
        )

    return {
        "id": estacion.id,
        "nombre": estacion.nombre,
        "metrica": metrica,
        "submetricas_disponibles": submetricas
    }

@router.get("/regiones", response_model=List[RegionSchema])
async def get_regiones_disponibles(db: Session = Depends(get_db)):
    """Obtener lista única de regiones que tienen estaciones con datos"""
    regiones = db.query(
        Estacion.numero_region,
        Estacion.nombre_region
    ).distinct().order_by(Estacion.numero_region).all()

    return [
        {"numero_region": r.numero_region, "nombre_region": r.nombre_region}
        for r in regiones
    ]

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
