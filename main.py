from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import create_db_and_tables, get_session
from app.routers import usuarios, peliculas, favoritos
from app.config import settings
from sqlmodel import Session, select
from sqlalchemy import func
from fastapi import Depends


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestor de ciclo de vida de la aplicación.
    Se ejecuta al iniciar y al cerrar la aplicación.
    """
    # Startup: Crear tablas en la base de datos
    create_db_and_tables()
    yield
    
    # Shutdown: Limpiar recursos si es necesario
    print("cerrando aplicación...")


# TODO: Crear la instancia de FastAPI con metadatos apropiados
# Incluir: title, description, version, contact, license_info
app = FastAPI(
    title="API de Películas",
    description="API RESTful para gestionar usuarios, películas y favoritos. Proyecto educativo Uniremington.",
    version="1.0.0",
    lifespan=lifespan,
    contact={
        "name": "Lina Chamorro",
        "email": "lina.chamorro@uniremington.edu.co",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
)


# TODO: Configurar CORS para permitir solicitudes desde diferentes orígenes
# Esto es importante para desarrollo con frontend separado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: En producción, especificar orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(usuarios.router)
app.include_router(peliculas.router)
app.include_router(favoritos.router)


# TODO: Crear un endpoint raíz que retorne información básica de la API
@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raíz de la API.
    Retorna información básica y enlaces a la documentación.
    """
    return {
        "mensaje": "Bienvenido a la API de Películas",
        "version": "1.0.0",
        "autora": "Lina Chamorro",
        "institución": "Uniremington",
        "documentacion": "/docs",
        "redoc": "/redoc",
        "repositorio": "https://github.com/life151/ip3-taller2-taller3",
        "endpoints": {
            "usuarios": "/api/usuarios",
            "peliculas": "/api/peliculas",
            "favoritos": "/api/favoritos",
            "estadisticas": "/api/estadisticas"
        }
    }


# Crear un endpoint de health check para monitoreo
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint para verificar el estado de la API.
    Útil para sistemas de monitoreo y orquestación.
    """
    from app.database import check_database_connection
    db_status = "connected" if check_database_connection() else "disconnected"

    return {
        "status": "healthy",
        "database": db_status,
        "environment": settings.environment,
        "version": "1.0.0"
    }


@app.get("/api/estadisticas/", tags=["Estadísticas"])
async def obtener_estadisticas_generales(session: Session = Depends(get_session)):
    """
    Obtiene estadísticas generales de la plataforma.

    Retorna:
    - Total de usuarios
    - Total de películas
    - Total de favoritos
    - Película más popular
    - Usuario más activo
    """
    from app.models import Usuario, Pelicula, Favorito

    total_usuarios = session.exec(select(func.count(Usuario.id))).one()
    total_peliculas = session.exec(select(func.count(Pelicula.id))).one()
    total_favoritos = session.exec(select(func.count(Favorito.id))).one()

    statement_pelicula = (
        select(Pelicula, func.count(Favorito.id).label("count"))
        .outerjoin(Favorito, Pelicula.id == Favorito.id_pelicula)
        .group_by(Pelicula.id)
        .order_by(func.count(Favorito.id).desc())
        .limit(1)
    )
    top_pelicula = session.exec(statement_pelicula).first()

    statement_usuario = (
        select(Usuario, func.count(Favorito.id).label("count"))
        .outerjoin(Favorito, Usuario.id == Favorito.id_usuario)
        .group_by(Usuario.id)
        .order_by(func.count(Favorito.id).desc())
        .limit(1)
    )
    top_usuario = session.exec(statement_usuario).first()

    return {
        "total_usuarios": total_usuarios,
        "total_peliculas": total_peliculas,
        "total_favoritos": total_favoritos,
        "pelicula_mas_popular": top_pelicula[0].titulo if top_pelicula and top_pelicula[1] > 0 else "Ninguna",
        "usuario_mas_activo": top_usuario[0].nombre if top_usuario and top_usuario[1] > 0 else "Ninguno"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )

