# Instrucciones de Uso - API de Películas

## Proyecto Fullstack
**Autora:** Lina Chamorro
**Institución:** Uniremington - Ingeniería de Sistemas
**Repositorio:** https://github.com/life151/ip3-taller2-taller3

## Descripción
Este proyecto integra un backend desarrollado con FastAPI y un frontend interactivo con HTML, CSS y JavaScript para gestionar películas, usuarios y favoritos.

## Requisitos
- Python 3.8 o superior
- Navegador web moderno (Chrome, Firefox, Edge, Safari)

## Instalación

### 1. Instalar dependencias del backend
```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
El archivo `.env` ya está configurado con valores predeterminados para desarrollo local.

## Ejecución

### Iniciar el servidor backend
```bash
python main.py
```

O alternativamente:
```bash
uvicorn main:app --reload
```

El servidor se ejecutará en: `http://127.0.0.1:8000`

### Acceder a la documentación de la API
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

### Abrir el frontend
1. Navega a la carpeta `lp3-taller3`
2. Abre el archivo `index.html` en tu navegador
3. O utiliza un servidor local:
   ```bash
   python -m http.server 8080
   ```
   Luego accede a: http://localhost:8080/lp3-taller3/

## Inicializar Base de Datos con Datos de Ejemplo

Si deseas poblar la base de datos con datos de ejemplo:

1. Abre DBeaver o cualquier cliente SQLite
2. Conecta a la base de datos `peliculas.db`
3. Ejecuta el script `init_db.sql`

## Estructura del Proyecto

```
├── app/
│   ├── models.py          # Modelos de datos
│   ├── schemas.py         # Esquemas Pydantic
│   ├── database.py        # Configuración de base de datos
│   ├── config.py          # Configuración de la aplicación
│   └── routers/
│       ├── usuarios.py    # Endpoints de usuarios
│       ├── peliculas.py   # Endpoints de películas
│       └── favoritos.py   # Endpoints de favoritos
├── lp3-taller3/          # Frontend
│   ├── index.html        # Página principal
│   ├── css/
│   │   └── styles.css    # Estilos
│   └── js/
│       ├── main.js       # Configuración principal
│       ├── usuarios.js   # Módulo de usuarios
│       ├── peliculas.js  # Módulo de películas
│       ├── favoritos.js  # Módulo de favoritos
│       └── estadisticas.js # Módulo de estadísticas
├── main.py              # Punto de entrada de la API
├── requirements.txt     # Dependencias Python
└── peliculas.db        # Base de datos SQLite

```

## Funcionalidades Implementadas

### Backend (API RESTful)
- CRUD completo de usuarios
- CRUD completo de películas
- Gestión de favoritos
- Búsqueda avanzada de películas
- Endpoint de estadísticas generales
- Validación de datos con Pydantic
- Documentación automática con Swagger/ReDoc

### Frontend
- Interfaz interactiva para gestionar usuarios
- Catálogo de películas con diseño de tarjetas
- Sistema de favoritos
- Dashboard de estadísticas
- Diseño responsivo
- Animaciones y transiciones suaves

## Endpoints Principales

### Usuarios
- `GET /api/usuarios/` - Listar usuarios
- `POST /api/usuarios/` - Crear usuario
- `GET /api/usuarios/{id}` - Obtener usuario
- `PUT /api/usuarios/{id}` - Actualizar usuario
- `DELETE /api/usuarios/{id}` - Eliminar usuario
- `GET /api/usuarios/{id}/favoritos` - Favoritos del usuario

### Películas
- `GET /api/peliculas/` - Listar películas
- `POST /api/peliculas/` - Crear película
- `GET /api/peliculas/{id}` - Obtener película
- `PUT /api/peliculas/{id}` - Actualizar película
- `DELETE /api/peliculas/{id}` - Eliminar película
- `GET /api/peliculas/buscar/` - Búsqueda avanzada
- `GET /api/peliculas/populares/top` - Películas más populares

### Favoritos
- `GET /api/favoritos/` - Listar favoritos
- `POST /api/favoritos/` - Crear favorito
- `GET /api/favoritos/{id}` - Obtener favorito
- `DELETE /api/favoritos/{id}` - Eliminar favorito

### Estadísticas
- `GET /api/estadisticas/` - Estadísticas generales de la plataforma

## Solución de Problemas

### Error: Base de datos no encontrada
Si la base de datos no existe, el sistema la creará automáticamente al iniciar el servidor.

### Error: Puerto 8000 en uso
Si el puerto 8000 está ocupado, puedes cambiar el puerto en el archivo `app/config.py` o ejecutar:
```bash
uvicorn main:app --port 8001
```

### Error: CORS
El CORS ya está configurado para permitir solicitudes desde cualquier origen en desarrollo. En producción, deberás especificar los orígenes permitidos.

## Contribuciones
Este es un proyecto educativo. Para contribuciones, por favor contacta a la autora.

## Licencia
MIT License - Proyecto Educativo
