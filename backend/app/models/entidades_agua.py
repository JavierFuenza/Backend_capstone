from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from core.database import Base

class EntidadAgua(Base):
    __tablename__ = "entidades_agua"
    __table_args__ = (
        UniqueConstraint('nombre', 'subtipo', name='uq_nombre_subtipo'),
        {"schema": "public"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    subtipo = Column(String(50), nullable=False, index=True)
    descripcion = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
