# API REST PTAS v1.0

## Base URL
```
http://localhost:8000/api/v1
```

## Autenticación

### POST /auth/login
Login de usuario, retorna JWT token.

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "admin@ptas.cl",
    "username": "admin",
    "full_name": "Administrador",
    "role": "administrador",
    "plant_id": 1
  }
}
```

### POST /auth/refresh
Refresca token de acceso.

### POST /auth/register
Registrar nuevo usuario (solo admin).

---

## Plantas

### GET /plants
Lista todas las plantas.

### GET /plants/{id}
Detalle de planta.

### POST /plants
Crear planta (admin).

### PUT /plants/{id}
Actualizar planta.

### DELETE /plants/{id}
Desactivar planta.

---

## Mediciones

### GET /measurements
Lista mediciones con filtros.

**Query Params:**
- `plant_id` (int)
- `phase` (string): afluente, pretratamiento, reactor, clarificador, desinfeccion, lodos
- `start_date` (date)
- `end_date` (date)
- `limit` (int, default 50)
- `offset` (int, default 0)

### GET /measurements/{id}
Detalle de medición.

### POST /measurements
Registrar nueva medición.

**Request:**
```json
{
  "plant_id": 1,
  "phase": "afluente",
  "timestamp": "2026-02-19T08:00:00",
  "caudal_affluent_m3h": 125.5,
  "ph": 7.2,
  "temperature": 18.5,
  "od": 2.1,
  "conductivity": 850.0,
  "sst": 180.0,
  "dbo5": 120.0,
  "dqo": 250.0,
  "level_sludge_m": 1.2,
  "notes": "Muestra tomada a las 8:00 AM"
 /measurements/{}
```

### PUTid}
Actualizar medición.

### POST /measurements/{id}/validate
Validar medición (supervisor/admin).

---

## Equipos

### GET /equipment
Lista equipos por planta.

**Query Params:**
- `plant_id` (int)
- `status` (string): active, inactive, maintenance, broken

### GET /equipment/{id}
Detalle de equipo.

### POST /equipment
Crear equipo.

### PUT /equipment/{id}
Actualizar equipo.

### GET /equipment/{id}/hours
Horas de operación del equipo.

### POST /equipment/{id}/hours
Registrar horas de operación.

---

## Alertas

### GET /alerts
Lista alertas.

**Query Params:**
- `plant_id` (int)
- `is_resolved` (bool)
- `severity` (string): low, medium, high, critical
- `alert_type` (string)
- `limit` (int)

### GET /alerts/{id}
Detalle de alerta.

### PUT /alerts/{id}/resolve
Resolver alerta.

**Request:**
```json
{
  "resolution_notes": "Problema resuelto, se ajustó el sistema de aireación"
}
```

### GET /alerts/stats
Estadísticas de alertas.

---

## Dashboard

### GET /dashboard/summary
Resumen ejecutivo de planta.

**Response:**
```json
{
  "plant": { "id": 1, "name": "PTAS La Serena" },
  "last_measurement": {
    "timestamp": "2026-02-19T08:00:00",
    "phase": "efluente",
    "caudal_effluent_m3h": 118.2,
    "ph": 7.1,
    "chlorine_free": 0.8,
    "sst": 15.0,
    "dbo5": 12.0
  },
  "compliance": {
    "ds90_compliant": true,
    "ds609_compliant": true,
    "last_violation": null
  },
  "alerts": {
    "active": 2,
    "critical": 0,
    "warning": 2
  },
  "equipment": {
    "total": 12,
    "active": 10,
    "maintenance": 1,
    "broken": 1
  },
  "stats": {
    "avg_caudal_last_30d": 120.5,
    "avg_ph_last_30d": 7.1,
    "compliance_rate_30d": 94.5
  }
}
```

### GET /dashboard/trends
Tendencias históricas.

**Query Params:**
- `plant_id` (int)
- `parameter` (string): ph, temperature, caudal, sst, dbo5, etc.
- `days` (int, default 30)

---

## Reportes

### GET /reports/monthly
Reporte mensual PDF.

**Query Params:**
- `plant_id` (int)
- `year` (int)
- `month` (int)

### GET /reports/compliance
Reporte de cumplimiento normativo.

---

## Códigos de Estado

| Código | Descripción |
|--------|-------------|
| 200 | OK |
| 201 | Creado |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

---

## Encabezados

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```
