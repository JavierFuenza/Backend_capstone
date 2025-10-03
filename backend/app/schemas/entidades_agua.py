from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EntidadAguaBase(BaseModel):
    nombre: str = Field(..., description="Nombre de la entidad de agua")
    subtipo: str = Field(..., description="Subtipo: estacion, cuenca, embalse, etc.")
    descripcion: Optional[str] = Field(None, description="Descripción de la entidad")

class EntidadAguaSchema(EntidadAguaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EntidadAguaCreate(EntidadAguaBase):
    """Schema para crear nuevas entidades de agua"""
    pass
