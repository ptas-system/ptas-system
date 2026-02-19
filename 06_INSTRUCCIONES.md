# Instrucciones de Ejecución - Sistema PTAS

## Requisitos Previos

- Docker
- Docker Compose

## Levantar el Sistema

```bash
cd /Users/patriciofloresfuentes/ptas-system
docker compose up --build -d
```

Esto levantará:
- **PostgreSQL** en puerto 5432
- **Backend FastAPI** en puerto 8000
- **Frontend React** en puerto 5173

## Verificar que esté funcionando

```bash
# Health check backend
curl http://localhost:8000/health

# Ver logs
docker compose logs -f
```

## Acceder a la Aplicación

1. Abrir en navegador: **http://localhost:5173**

2. Credenciales por defecto:
   - **Usuario:** `admin`
   - **Contraseña:** `admin123`

## Endpoints Útiles

| Endpoint | Descripción |
|----------|-------------|
| http://localhost:8000 | API Root |
| http://localhost:8000/docs | Swagger/OpenAPI |
| http://localhost:5173 | Frontend React |

## Comandos Adicionales

```bash
# Detener servicios
docker compose down

# Reiniciar servicios
docker compose restart

# Ver logs de un servicio
docker compose logs -f backend
docker compose logs -f frontend

# Eliminar datos (reset)
docker compose down -v
```

## Estructura de Datos Inicial

Al iniciar se crea automáticamente:
- Usuario: `admin` / `admin123` (rol: administrador)
- Planta: `PTAS demo` (código: PTAS-001)

## Notas

- El backend espera a que PostgreSQL estéhealthy antes de iniciar
- El frontend hace proxy a `/api` → backend:8000
- Los datos persisten en volumen Docker `postgres_data`
