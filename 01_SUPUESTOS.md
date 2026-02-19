# Supuestos del Sistema PTAS v1.0

## 1. Supuestos Técnicos

| Supuesto | Detalle |
|----------|---------|
| **Autenticación** | JWT con tokens de acceso de 60 min y refresh de 7 días |
| **Contraseñas** | Hasheadas con bcrypt (12 rounds) |
| **TZ** | Chile continental (UTC-3 / UTC-4 DST) |
| **Moneda** | CLP para costos, USD para métricas |
| **Decimal** | Separador punto, 2 decimales para parámetros |
| **Fechas** | ISO 8601, formato `YYYY-MM-DDTHH:MM:SS` |

## 2. Supuestos Operativos

| Supuesto | Detalle |
|----------|---------|
| **Registro manual** | Principal método de entrada (MVP) |
| **Frecuencia** | Datos diarios mínimo, preferible 3-4/turno |
| **Plantas** | Multi-planta soportado (1-50) |
| **Usuarios/planta** | 1-20 usuarios |
| **Alertas** | Email + dashboard (SMS futuro) |

## 3. Supuestos Normativos (Chile)

| Norma | Parámetros | Límites DS90 |
|-------|------------|--------------|
| **DS 90** | pH | 6.0 - 9.0 |
| | Temperatura | ≤ 35°C |
| | SST | ≤ 80 mg/L |
| | DBO5 | ≤ 60 mg/L |
| | Grasas y Aceites | ≤ 100 mg/L |
| | Coliformes Fecales | ≤ 1000 NMP/100mL |

| Norma | Parámetros | Límites DS609 |
|-------|------------|--------------|
| **DS 609** | Cloro libre efluente | ≥ 0.5 mg/L (mínimo) |
| | pH efluente | 6.5 - 8.5 |
| | Turbiedad | ≤ 2 NTU (recomendado) |

## 4. Supuestos de Infraestructura

| Item | Valor |
|------|-------|
| **Contenedores** | 3 (backend, frontend, postgres) |
| **Recursos mínimos** | 2CPU, 4GB RAM |
| **Almacenamiento** | 10GB mínimo |
| **Backups** | Daily auto (7 días retención) |

## 5. Supuestos de IA (MVP)

| Capacidad | Enfoque |
|-----------|---------|
| **Detección anomalías** | Reglas estadísticas (IQR, z-score) |
| **Alertas** | Threshold configurable por usuario |
| **Predicción** | No en MVP (futuro: LSTM/Prophet) |
| **Recomendaciones** | Basadas en reglas heurísticas |

## 6. Supuestos No Incluidos (Futuro)

- IoT / Sensores en tiempo real
- Integración con SCADA
- Módulo de facturación
- App móvil nativa
- API pública
- Machine learning avanzado
