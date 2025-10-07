from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from core.database import Base

class EntidadAgua(Base):
    __tablename__ = "entidades_agua"
    __table_args__ = (
        UniqueConstraint('nombre', 'tipo', name='uq_nombre_tipo'),
        {"schema": "public"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    tipo = Column(String(100), nullable=False, index=True)
    descripcion = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
