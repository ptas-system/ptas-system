# Modelo de Base de Datos PTAS

## Diagrama ER

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    users     │       │    plants    │       │ equipment    │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id (PK)      │◄──────│ id (PK)      │       │ id (PK)      │
│ email        │       │ name         │       │ name         │
│ username     │       │ code         │       │ type         │
│ password_hash│       │ address      │       │ plant_id (FK)│
│ full_name    │       │ capacity_m3 │       │ status       │
│ role         │       │ status       │       │ install_date │
│ plant_id (FK)│       │ created_at   │       │ hours_total  │
│ is_active    │       └──────────────┘       └──────────────┘
│ created_at   │              │                       │
└──────────────┘              │                       │
       │                     │                       │
       │                     │                       │
       ▼                     ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                      measurements                               │
├─────────────────────────────────────────────────────────────────┤
│ id (PK)                                                        │
│ plant_id (FK)          │ timestamp (fecha/hora)                 │
│ user_id (FK)          │ fase (afluente/pretratamiento/reactor/ │
│                        │         clarificador/desinfeccion/lodos)              │
│ caudal_affluent_m3h   │ caudal_effluent_m3h                   │
│ ph                    │ temperature                             │
│ od (oxygen dissolved) │ conductivity                           │
│ chlorine_free         │ sst (solids suspended total)            │
│ dbo5                  │ dqo                                     │
│ level_sludge_m        │ notes                                  │
│ created_at            │ validated                              │
└─────────────────────────────────────────────────────────────────┘
              │
              │
              ▼
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  equipment   │       │   alerts     │       │ equipment_   │
│  hours       │       │               │       │  hours       │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id (PK)      │       │ id (PK)      │       │ id (PK)      │
│ equipment_id │       │ plant_id (FK)│       │ equipment_id │
│ date         │       │ measurement_id       │ date         │
│ hours        │       │ type (warning/       │ hours        │
│ notes        │       │        critical/info)│ │ notes       │
│ created_at   │       │ title               │ │ created_at  │
│              │       │ message             │ └──────────────┘
│              │       │ ds90_violation      │
│              │       │ ds609_violation     │
│              │       │ is_resolved         │
│              │       │ resolved_at         │
│              │       │ resolved_by (FK)    │
│              │       │ created_at          │
└──────────────┘       └──────────────┘
```

## Tablas Detalladas

### 1. users (Usuarios)

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'operador',
    -- Roles: administrador, supervisor, operador
    plant_id INTEGER REFERENCES plants(id) ON DELETE SET NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. plants (Plantas)

```sql
CREATE TABLE plants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    -- Código interno (ej: PTAS-001)
    address TEXT,
    region VARCHAR(100),
    -- Región Chile
    capacity_m3d INTEGER,
    -- Capacidad m3/día
    population_equiv INTEGER,
    -- Habitantes equivalentes
    treatment_type VARCHAR(100),
    -- Tipo: lodos activados, fan, etc.
    status VARCHAR(50) DEFAULT 'active',
    -- active, inactive, maintenance
    ds90_enabled BOOLEAN DEFAULT TRUE,
    ds609_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. measurements (Mediciones)

```sql
CREATE TABLE measurements (
    id SERIAL PRIMARY KEY,
    plant_id INTEGER NOT NULL REFERENCES plants(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE SET NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Fase del proceso
    phase VARCHAR(50) NOT NULL,
    -- afluente, pretratamiento, reactor, clarificador, desinfeccion, lodos
    
    -- Parámetros hidráulicos
    caudal_affluent_m3h DECIMAL(10,3),
    caudal_effluent_m3h DECIMAL(10,3),
    
    -- Parámetros físicos
    ph DECIMAL(5,2),
    temperature DECIMAL(5,2),
    conductivity DECIMAL(10,2),
    turbidity DECIMAL(10,2),
    
    -- Parámetros químicos
    od DECIMAL(6,2),
    -- Oxígeno Disuelto (mg/L)
    chlorine_free DECIMAL(6,2),
    -- Cloro libre (mg/L)
    
    -- Parámetros orgánicos
    sst DECIMAL(10,2),
    -- Sólidos Suspendidos Totales (mg/L)
    dbo5 DECIMAL(10,2),
    dqo DECIMAL(10,2),
    
    -- Lodos
    level_sludge_m DECIMAL(5,3),
    -- Nivel de lodo en metro
    
    -- Observaciones
    notes TEXT,
    
    -- Validación
    validated BOOLEAN DEFAULT FALSE,
    validated_by INTEGER REFERENCES users(id),
    validated_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. equipment (Equipos)

```sql
CREATE TABLE equipment (
    id SERIAL PRIMARY KEY,
    plant_id INTEGER NOT NULL REFERENCES plants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50),
    equipment_type VARCHAR(100) NOT NULL,
    -- tipo: bomba, motor, soplador, mezclador, decantador, etc.
    brand VARCHAR(100),
    model VARCHAR(100),
    serial_number VARCHAR(100),
    power_kw DECIMAL(6,2),
    -- Potencia en kW
    status VARCHAR(50) DEFAULT 'active',
    -- active, inactive, maintenance, broken
    install_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. equipment_hours (Horas de Equipo)

```sql
CREATE TABLE equipment_hours (
    id SERIAL PRIMARY KEY,
    equipment_id INTEGER NOT NULL REFERENCES equipment(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    hours_run DECIMAL(5,2) NOT NULL,
    -- Horas de operación
    energy_kwh DECIMAL(10,2),
    -- Consumo energético
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(equipment_id, date)
);
```

### 6. alerts (Alertas)

```sql
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    plant_id INTEGER NOT NULL REFERENCES plants(id) ON DELETE CASCADE,
    measurement_id INTEGER REFERENCES measurements(id) ON DELETE SET NULL,
    equipment_id INTEGER REFERENCES equipment(id) ON DELETE SET NULL,
    
    alert_type VARCHAR(50) NOT NULL,
    -- warning, critical, info, ds90_violation, ds609_violation
    
    severity VARCHAR(20) NOT NULL,
    -- low, medium, high, critical
    
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    
    -- Referencia normativa
    ds90_violation BOOLEAN DEFAULT FALSE,
    ds609_violation BOOLEAN DEFAULT FALSE,
    norm_reference VARCHAR(100),
    -- DS90 Art. 3.a, etc.
    
    -- Estado
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_by INTEGER REFERENCES users(id),
    resolved_at TIMESTAMP,
    resolution_notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 7. maintenance_events (Eventos de Mantención)

```sql
CREATE TABLE maintenance_events (
    id SERIAL PRIMARY KEY,
    plant_id INTEGER NOT NULL REFERENCES plants(id) ON DELETE CASCADE,
    equipment_id INTEGER REFERENCES equipment(id) ON DELETE CASCADE,
    
    event_type VARCHAR(50) NOT NULL,
    -- preventivo, correctivo, predictivo
    
    title VARCHAR(255) NOT NULL,
    description TEXT,
    
    scheduled_date DATE,
    completed_date DATE,
    
    cost_clp DECIMAL(12,2),
    
    performed_by VARCHAR(255),
    
    status VARCHAR(50) DEFAULT 'scheduled',
    -- scheduled, in_progress, completed, cancelled
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Índices

```sql
-- Mediciones por planta y fecha
CREATE INDEX idx_measurements_plant_timestamp ON measurements(plant_id, timestamp DESC);

-- Alertas por planta y estado
CREATE INDEX idx_alerts_plant_resolved ON alerts(plant_id, is_resolved, created_at DESC);

-- Horas de equipo
CREATE INDEX idx_equipment_hours_equipment_date ON equipment_hours(equipment_id, date);
```

## Datos Iniciales

```sql
-- Usuario admin por defecto
-- Email: admin@ptas.cl
-- Password: admin123
-- Username: admin
```

## Notas

- Todos los timestamps en UTC-3 (Chile)
- FK con ON DELETE SET NULL para mantener integridad histórica
- Mediciones no se borran, se marcan como validadas/no validadas
- Alertas nunca se borran (historial)
