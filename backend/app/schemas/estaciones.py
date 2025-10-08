from pydantic import BaseModel, Field
from typing import Optional
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
