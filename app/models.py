"""
Modelos de datos usando SQLModel.
Define la estructura de las tablas de la base de datos.
SQLModel combina SQLAlchemy con Pydantic para validación automática.
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class Usuario(SQLModel, table=True):
    """
    Modelo de Usuario.
    Representa a los usuarios registrados en la plataforma.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, index=True)
    correo: str = Field(unique=True, max_length=150, index=True)
    fecha_registro: datetime = Field(default_factory=datetime.now)

    favoritos: List["Favorito"] = Relationship(back_populates="usuario", cascade_delete=True)

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre={self.nombre}, correo={self.correo})>"

    @property
    def cantidad_favoritos(self) -> int:
        return len(self.favoritos) if self.favoritos else 0


class Pelicula(SQLModel, table=True):
    """
    Modelo de Película.
    Representa las películas disponibles en la plataforma.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(max_length=200, index=True)
    director: str = Field(max_length=150)
    genero: str = Field(max_length=100)
    duracion: int = Field(description="Duración en minutos")
    año: int = Field(ge=1888, le=2100)
    clasificacion: str = Field(max_length=10)
    sinopsis: Optional[str] = Field(default=None, max_length=1000)
    fecha_creacion: datetime = Field(default_factory=datetime.now)

    favoritos: List["Favorito"] = Relationship(back_populates="pelicula", cascade_delete=True)

    def __repr__(self):
        return f"<Pelicula(id={self.id}, titulo={self.titulo}, año={self.año})>"


class Favorito(SQLModel, table=True):
    """
    Modelo de Favorito.
    Representa la relación muchos-a-muchos entre usuarios y películas.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuario.id", ondelete="CASCADE")
    id_pelicula: int = Field(foreign_key="pelicula.id", ondelete="CASCADE")
    fecha_marcado: datetime = Field(default_factory=datetime.now)

    usuario: Optional[Usuario] = Relationship(back_populates="favoritos")
    pelicula: Optional[Pelicula] = Relationship(back_populates="favoritos")

    def __repr__(self):
        return f"<Favorito(id={self.id}, usuario_id={self.id_usuario}, pelicula_id={self.id_pelicula})>"

