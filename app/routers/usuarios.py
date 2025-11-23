"""
Router de Usuarios.
Endpoints para gestionar usuarios en la plataforma.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models import Usuario, Favorito, Pelicula
from app.schemas import (
    UsuarioCreate,
    UsuarioRead,
    UsuarioUpdate,
    UsuarioWithFavoritos,
    PeliculaRead
)

router = APIRouter(
    prefix="/api/usuarios",
    tags=["Usuarios"]
)


@router.get("/", response_model=List[UsuarioRead])
def listar_usuarios(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    """
    Lista todos los usuarios registrados.

    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a retornar
    """
    statement = select(Usuario).offset(skip).limit(limit)
    usuarios = session.exec(statement).all()
    return usuarios


@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    usuario: UsuarioCreate,
    session: Session = Depends(get_session)
):
    """
    Crea un nuevo usuario en la plataforma.

    - **nombre**: Nombre del usuario
    - **correo**: Correo electrónico único
    """
    statement = select(Usuario).where(Usuario.correo == usuario.correo)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario con el correo '{usuario.correo}'"
        )

    db_usuario = Usuario.model_validate(usuario)
    session.add(db_usuario)
    session.commit()
    session.refresh(db_usuario)

    return db_usuario


@router.get("/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(
    usuario_id: int,
    session: Session = Depends(get_session)
):
    """
    Obtiene un usuario específico por su ID.

    - **usuario_id**: ID del usuario
    """
    usuario = session.get(Usuario, usuario_id)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {usuario_id} no encontrado"
        )

    return usuario


@router.put("/{usuario_id}", response_model=UsuarioRead)
def actualizar_usuario(
    usuario_id: int,
    usuario_update: UsuarioUpdate,
    session: Session = Depends(get_session)
):
    """
    Actualiza la información de un usuario existente.

    - **usuario_id**: ID del usuario a actualizar
    - **nombre**: Nuevo nombre (opcional)
    - **correo**: Nuevo correo (opcional)
    """
    db_usuario = session.get(Usuario, usuario_id)

    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {usuario_id} no encontrado"
        )

    if usuario_update.correo and usuario_update.correo != db_usuario.correo:
        statement = select(Usuario).where(Usuario.correo == usuario_update.correo)
        existing_user = session.exec(statement).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un usuario con el correo '{usuario_update.correo}'"
            )

    usuario_data = usuario_update.model_dump(exclude_unset=True)
    for key, value in usuario_data.items():
        setattr(db_usuario, key, value)

    session.add(db_usuario)
    session.commit()
    session.refresh(db_usuario)

    return db_usuario


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(
    usuario_id: int,
    session: Session = Depends(get_session)
):
    """
    Elimina un usuario de la plataforma.

    - **usuario_id**: ID del usuario a eliminar

    También se eliminarán todos los favoritos asociados al usuario.
    """
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {usuario_id} no encontrado"
        )

    session.delete(usuario)
    session.commit()
    return None


@router.get("/{usuario_id}/favoritos", response_model=List[PeliculaRead])
def listar_favoritos_usuario(
    usuario_id: int,
    session: Session = Depends(get_session)
):
    """
    Lista todas las películas favoritas de un usuario.

    - **usuario_id**: ID del usuario
    """
    usuario = session.get(Usuario, usuario_id)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {usuario_id} no encontrado"
        )

    statement = (
        select(Pelicula)
        .join(Favorito)
        .where(Favorito.id_usuario == usuario_id)
    )
    peliculas = session.exec(statement).all()

    return peliculas


@router.post(
    "/{usuario_id}/favoritos/{pelicula_id}",
    status_code=status.HTTP_201_CREATED
)
def marcar_favorito(
    usuario_id: int,
    pelicula_id: int,
    session: Session = Depends(get_session)
):
    """
    Marca una película como favorita para un usuario.

    - **usuario_id**: ID del usuario
    - **pelicula_id**: ID de la película
    """
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {usuario_id} no encontrado"
        )

    pelicula = session.get(Pelicula, pelicula_id)
    if not pelicula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Película con id {pelicula_id} no encontrada"
        )

    statement = select(Favorito).where(
        Favorito.id_usuario == usuario_id,
        Favorito.id_pelicula == pelicula_id
    )
    existing_favorito = session.exec(statement).first()
    if existing_favorito:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La película ya está marcada como favorita"
        )

    favorito = Favorito(id_usuario=usuario_id, id_pelicula=pelicula_id)
    session.add(favorito)
    session.commit()

    return {"message": "Película marcada como favorita exitosamente"}


@router.delete(
    "/{usuario_id}/favoritos/{pelicula_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def eliminar_favorito(
    usuario_id: int,
    pelicula_id: int,
    session: Session = Depends(get_session)
):
    """
    Elimina una película de los favoritos de un usuario.

    - **usuario_id**: ID del usuario
    - **pelicula_id**: ID de la película
    """
    statement = select(Favorito).where(
        Favorito.id_usuario == usuario_id,
        Favorito.id_pelicula == pelicula_id
    )
    favorito = session.exec(statement).first()

    if not favorito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El favorito no existe"
        )

    session.delete(favorito)
    session.commit()
    return None


@router.get("/{usuario_id}/estadisticas")
def obtener_estadisticas_usuario(
    usuario_id: int,
    session: Session = Depends(get_session)
):
    """
    Obtiene estadísticas del usuario (películas favoritas, géneros preferidos, etc.)

    - **usuario_id**: ID del usuario
    """
    usuario = session.get(Usuario, usuario_id)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {usuario_id} no encontrado"
        )

    from sqlalchemy import func

    total_favoritos = session.exec(
        select(func.count(Favorito.id)).where(Favorito.id_usuario == usuario_id)
    ).one()

    statement_peliculas = (
        select(Pelicula)
        .join(Favorito)
        .where(Favorito.id_usuario == usuario_id)
    )
    peliculas = session.exec(statement_peliculas).all()

    generos = {}
    tiempo_total = 0
    for pelicula in peliculas:
        tiempo_total += pelicula.duracion
        for genero in pelicula.genero.split(", "):
            generos[genero] = generos.get(genero, 0) + 1

    genero_favorito = max(generos.items(), key=lambda x: x[1])[0] if generos else None

    return {
        "usuario": usuario.nombre,
        "total_favoritos": total_favoritos,
        "tiempo_total_minutos": tiempo_total,
        "tiempo_total_horas": round(tiempo_total / 60, 2),
        "genero_favorito": genero_favorito,
        "distribucion_generos": generos
    }
