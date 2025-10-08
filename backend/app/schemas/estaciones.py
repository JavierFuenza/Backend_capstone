from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class EstacionBase(BaseModel):
    nombre: str = Field(..., description="Nombre de la estación")
    latitud: float = Field(..., description="Latitud en formato decimal")
    longitud: float = Field(..., description="Longitud en formato decimal")
    numero_region: int = Field(..., description="Número de la región (1-16)")
    nombre_region: str = Field(..., max_length=100, description="Nombre de la región")
    descripcion: Optional[str] = Field(None, description="Descripción de la estación")

class EstacionSchema(EstacionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class EstacionCreate(EstacionBase):
    """Schema para crear nuevas estaciones (si lo necesitas en el futuro)"""
    pass

class RegionSchema(BaseModel):
    numero_region: int = Field(..., description="Número de la región")
    nombre_region: str = Field(..., description="Nombre de la región")

    class Config:
        from_attributes = True

class EstacionMetricasSchema(BaseModel):
    id: int = Field(..., description="ID de la estación")
    nombre: str = Field(..., description="Nombre de la estación")
    descripcion: Optional[str] = Field(None, description="Descripción de la estación")
    metricas_disponibles: List[str] = Field(..., description="Lista de categorías de métricas disponibles")

    class Config:
        from_attributes = True

class EstacionSubmetricasSchema(BaseModel):
    id: int = Field(..., description="ID de la estación")
    nombre: str = Field(..., description="Nombre de la estación")
    metrica: str = Field(..., description="Categoría de métrica consultada")
    submetricas_disponibles: List[str] = Field(..., description="Lista de submmétricas específicas disponibles")

    class Config:
        from_attributes = True
