# VIS-1 — Arquitectura base, infraestructura (AWS) y CI/CD

| Campo | Valor |
|---|---|
| Ticket | [VIS-1](https://linear.app/parrot-apps/issue/VIS-1/vis-1-arquitectura-base-infraestructura-aws-y-cicd) |
| Estado | Backlog |
| Prioridad | Urgent |
| Labels | ninguna |
| Rama sugerida | `feature/VIS-1` |
| Estrategia generada | 2026-06-18 |

> Lee primero `docs/tickets/_ARQUITECTURA.md` para el stack y la estructura de repositorio objetivo. Proyecto nuevo: las rutas citadas son a crear.

## 1. Contexto y objetivo
Ticket fundacional del proyecto Visitor. Crea el esqueleto del repositorio para los tres clientes (web, móvil, backend), define entornos, aprovisiona la infraestructura cloud y monta el pipeline de CI/CD. Sin esta base, el resto de tickets no tiene dónde construirse.

## 2. Alcance
- **Incluye:** estructura de repositorio; configuración base de cada app; entornos dev/staging/producción; infraestructura AWS (cómputo, PostgreSQL gestionado, almacenamiento de archivos, gestión de secretos); pipeline CI/CD con lint/build/test/deploy; HTTPS/TLS y dominios; estrategia de backups.
- **No incluye:** lógica de negocio, autenticación (VIS-2), modelo de datos (VIS-3). Solo el andamiaje.

## 3. Análisis técnico
No existe código aún. Se parte de cero siguiendo el stack del PRD §6 (React+TS web, React Native+TS móvil, Python/FastAPI backend, PostgreSQL, AWS). Decisiones a validar antes de codificar: monorepo vs multi-repo (se sugiere monorepo `visitor/apps/{api,web,mobile}`), FastAPI vs Django (se sugiere FastAPI + SQLAlchemy + Alembic), y Vite vs Next.js para web.

## 4. Plan de implementación
1. Crear el monorepo con la estructura de `_ARQUITECTURA.md` (`apps/api`, `apps/web`, `apps/mobile`, `docs/`).
2. **Backend** (`apps/api`): inicializar proyecto FastAPI, `app/main.py` con healthcheck `/health`, `app/core/config.py` (variables de entorno), conexión a PostgreSQL y Alembic vacío en `app/db/migrations`.
3. **Web** (`apps/web`): inicializar React + TypeScript, ESLint/Prettier, estructura `src/{routes,pages,components,store,api,i18n}`, pantalla placeholder.
4. **Móvil** (`apps/mobile`): inicializar React Native + TypeScript, estructura `src/{navigation,screens,components,store,api,i18n}`, pantalla placeholder.
5. **Infraestructura**: definir IaC (Terraform o CDK) para VPC, RDS PostgreSQL, cómputo (ECS/Fargate o EC2), bucket de archivos (S3), y secretos (Secrets Manager/SSM). Configurar dominios y certificados TLS (ACM).
6. **CI/CD**: pipeline (GitHub Actions u opción equivalente) con jobs de lint, build y test por app, y deploy por entorno (dev/staging/prod).
7. **Backups**: habilitar snapshots automáticos de RDS, versionado de S3 y respaldo del repositorio.
8. Documentar arranque local reproducible en `README` y variables de entorno de ejemplo (`.env.example`).

## 5. Datos y migraciones
Configurar la conexión a PostgreSQL y Alembic, pero **sin tablas de negocio** (eso es VIS-3). Solo dejar la herramienta de migraciones lista.

## 6. i18n
Dejar el scaffolding de i18n en web y móvil con idioma base inglés (sin claves de negocio todavía). Detalle en VIS-19.

## 7. Criterios de aceptación
- Las tres apps arrancan en local con instrucciones reproducibles.
- Existen entornos dev/staging/producción separados.
- El pipeline ejecuta lint/build/test y despliega automáticamente.
- HTTPS forzado en entornos accesibles.
- Backups configurados y restaurables (probar una restauración).

## 8. Pruebas y verificación
Levantar cada app localmente; ejecutar el pipeline en una rama de prueba; desplegar a dev; verificar `/health`; ejecutar una restauración de backup de RDS en un entorno aislado.

## 9. Riesgos y consideraciones
Elección de FastAPI vs Django y Vite vs Next.js condiciona todos los tickets siguientes: cerrarla aquí. Costos AWS de RDS y cómputo. La complejidad de IaC puede crecer; empezar mínimo y escalar.

## 10. Dependencias
Ninguna. **Bloquea** a todos los demás tickets (VIS-2 … VIS-19).
