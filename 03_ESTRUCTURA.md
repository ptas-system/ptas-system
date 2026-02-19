# Estructura del Repositorio PTAS

```
ptas-system/
├── 01_SUPUESTOS.md           # Supuestos técnicos y normativos
├── 02_ARQUITECTURA.md        # Diagrama de arquitectura
├── 03_ESTRUCTURA.md          # Este archivo
├── 04_DATABASE.md            # Modelo de datos
├── 05_API.md                 # Documentación API
├── 06_INSTRUCCIONES.md       # Guía de ejecución
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entrypoint
│   │   │
│   │   ├── core/                # Configuración central
│   │   │   ├── __init__.py
│   │   │   ├── config.py        # Settings
│   │   │   ├── security.py     # JWT, password hashing
│   │   │   └── database.py      # Conexión DB
│   │   │
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── plant.py
│   │   │   ├── measurement.py
│   │   │   ├── equipment.py
│   │   │   └── alert.py
│   │   │
│   │   ├── schemas/             # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── plant.py
│   │   │   ├── measurement.py
│   │   │   └── equipment.py
│   │   │
│   │   ├── routers/            # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── plants.py
│   │   │   ├── measurements.py
│   │   │   ├── equipment.py
│   │   │   ├── alerts.py
│   │   │   └── reports.py
│   │   │
│   │   ├── services/            # Lógica de negocio
│   │   │   ├── __init__.py
│   │   │   ├── ia_engine.py    # Motor IA
│   │   │   ├── normativity.py  # DS90/DS609
│   │   │   └── alerts.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── validators.py
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   └── alembic/
│       ├── env.py
│       └── versions/
│
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── index.css
│   │   │
│   │   ├── types/
│   │   │   └── index.ts        # TypeScript interfaces
│   │   │
│   │   ├── services/
│   │   │   ├── api.ts          # Axios instance
│   │   │   └── auth.ts         # Auth functions
│   │   │
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   └── useApi.ts
│   │   │
│   │   ├── components/
│   │   │   ├── Layout.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Header.tsx
│   │   │   └── Card.tsx
│   │   │
│   │   └── pages/
│   │       ├── Login.tsx
│   │       ├── Dashboard.tsx
│   │       ├── Measurements.tsx
│   │       ├── Equipment.tsx
│   │       └── Alerts.tsx
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── docker-compose.yml
├── .env.example
└── README.md
```

## Convenciones

| Item | Convención |
|------|------------|
| **Ramas** | `feature/`, `bugfix/`, `hotfix/` |
| **Commits** | Conventional: `feat:`, `fix:`, `docs:` |
| **Python** | snake_case, PEP8 |
| **TypeScript** | camelCase, ESLint |
| **Git** | Main branch: `main` |
