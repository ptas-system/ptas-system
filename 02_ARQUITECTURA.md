# Arquitectura General del Sistema PTAS

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CLIENTE (Frontend)                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │    Login    │  │  Dashboard  │  │ Mediciones │  │   Equipos   │      │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘      │
│         │                │                │                │              │
│         └────────────────┴────────────────┴────────────────┘              │
│                                    │                                       │
│                           ┌────────▼────────┐                             │
│                           │   React Router   │                             │
│                           │   + Context API  │                             │
│                           └────────┬────────┘                             │
└────────────────────────────────────┼───────────────────────────────────────┘
                                     │ HTTPS (443)
                                     │ JWT Auth
┌────────────────────────────────────┼───────────────────────────────────────┐
│                           SERVIDOR (Backend)                                │
│                           ┌────────▼────────┐                             │
│                           │   FastAPI        │                             │
│                           │   (Port 8000)    │                             │
│                           └────────┬────────┘                             │
│                                    │                                       │
│         ┌──────────────────────────┼──────────────────────────┐           │
│         │                          │                          │           │
│  ┌──────▼──────┐          ┌───────▼───────┐         ┌───────▼───────┐   │
│  │   Routers   │          │    Services    │         │     Core      │   │
│  │              │          │                │         │                │   │
│  │ - auth      │          │ - measurement  │         │ - config      │   │
│  │ - plants    │          │ - plant        │         │ - security    │   │
│  │ - measure   │          │ - equipment    │         │ - utils       │   │
│  │ - equipment │          │ - alerts       │         └────────────────   │
│  │ - alerts    │          │ - ia_engine    │                               │
│  │ - reports   │          └─────────────────┘                               │
│  └──────┬──────┘                                                              │
│         │                                                                     │
│  ┌──────▼──────┐          ┌──────────────────────────────────────────┐     │
│  │   Models    │          │              SQLAlchemy ORM               │     │
│  │  (Tables)   │◄────────►│                                          │     │
│  └─────────────┘          └──────────────────┬───────────────────────┘     │
│                                               │                             │
└───────────────────────────────────────────────┼─────────────────────────────┘
                                                │
                                 ┌──────────────▼──────────────┐
                                 │     PostgreSQL (Port 5432)  │
                                 │                            │
                                 │  - usuarios               │
                                 │  - plantas                │
                                 │  - mediciones             │
                                 │  - equipos                │
                                 │  - alertas                │
                                 │  - logs                   │
                                 └────────────────────────────┘


## Flujo de Datos

```
Usuario → Frontend → API (JWT) → Router → Service → Model → DB
                            ↓
                      IA Engine
                            ↓
                      Alertas/Recomendaciones
```

## Capas del Sistema

| Capa | Responsabilidad |
|------|-----------------|
| **Presentation** | UI React, componentes, páginas |
| **API** | FastAPI routers, validación, auth |
| **Business** | Services, reglas de negocio, IA |
| **Data** | SQLAlchemy models, migrations |
| **Infra** | Docker, PostgreSQL, backups |

## Seguridad

- JWT Bearer tokens
- Password hashing bcrypt
- CORS configurado
- Rate limiting (opcional)
- HTTPS en producción
