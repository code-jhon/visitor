# Visitor — Referencia de arquitectura (para agentes implementadores)

Documento de apoyo compartido por todas las estrategias de ticket (`VIS-N.md`).
Como el proyecto es nuevo, los archivos citados en los planes son **rutas
objetivo a crear**, no archivos existentes. Esta es la convención que todos los
tickets deben respetar.

## Stack (PRD §6)

- **Web:** React + TypeScript (Vite o Next.js a validar), gestión de estado con
  Redux Toolkit o Zustand, data-fetching con React Query.
- **Móvil:** React Native + TypeScript (Android + iOS).
- **Backend:** Python con FastAPI (preferido) o Django. ORM SQLAlchemy +
  Alembic para migraciones si se usa FastAPI.
- **Base de datos:** PostgreSQL.
- **Infraestructura:** AWS o equivalente.

Estas decisiones **reemplazan** las referencias históricas de la propuesta a
Angular, Ionic, Laravel/PHP y MySQL.

## Estructura de repositorio objetivo (monorepo sugerido)

```
visitor/
  apps/
    api/                 # Backend Python/FastAPI
      app/
        main.py
        core/            # config, security (JWT, hashing), permissions (RBAC)
        db/
          models/        # modelos SQLAlchemy
          migrations/    # Alembic
        api/routers/     # routers por dominio (auth, employees, visits, ...)
        services/        # lógica de negocio (scheduling, financial, reports, ...)
        schemas/         # Pydantic
        workers/         # tareas async/cron (auto-finalización, alertas)
    web/                 # Frontend React + TS
      src/
        routes/          # routing
        pages/           # vistas por módulo
        features/        # lógica por dominio
        components/      # UI compartida
        store/           # estado global
        api/             # cliente HTTP
        i18n/            # internacionalización (base: en)
    mobile/              # React Native + TS
      src/
        navigation/
        screens/
        components/
        store/
        api/
        i18n/
  docs/                  # PRD, propuesta, screens, tickets/
```

## Roles del sistema (PRD §4)

Admin, Empresa, Empleado, Proveedor/Coordinador, Cliente/Paciente, Soporte.
Todo endpoint y vista respeta RBAC (ver VIS-2).

## Restricciones transversales que todo plan debe respetar

- **Seguridad de datos de salud:** datos sensibles de pacientes con visibilidad
  por rol; cifrado en tránsito (HTTPS/TLS) y en reposo donde corresponda; hash
  seguro de contraseñas; validación/saneamiento de entradas (ver VIS-4).
- **Auditoría:** cambios importantes y eventos de ciclo de vida de visita
  registran actor, timestamp, acción, entidad, antes/después y geolocalización
  donde aplique (ver VIS-4).
- **Consistencia web/móvil:** el estado de visitas debe ser consistente entre
  clientes; la fuente de verdad es el backend.
- **TypeScript estricto** en web y móvil (sin `any`). Tipado/validación con
  Pydantic en el backend.
- **i18n:** idioma base inglés; estructurar para multilenguaje futuro.
- **Búsqueda y ayuda:** cada módulo web principal incluye searchbox por
  criterios definidos y botón de ayuda (ver VIS-19).

## Convención de ramas

`feature/VIS-N` (p. ej. `feature/VIS-10`), donde N es el número del ticket de
Linear. Coincide con el identificador nativo de Linear (sin ceros a la
izquierda).

## Plan de entregas (PRD §12)

- **Entrega 1 (30%):** VIS-1, VIS-2, VIS-3, VIS-5, VIS-6, VIS-7, VIS-8, VIS-9 y
  base de VIS-10.
- **Entrega 2 (30%):** VIS-10 completo, VIS-11, VIS-12, VIS-14, VIS-15, VIS-18.
- **Entrega 3 (40%):** VIS-4 (hardening), VIS-13, VIS-16, VIS-17, VIS-19, QA,
  despliegue y documentación.

## Preguntas abiertas del PRD (§14) que afectan a varios tickets

País/marco legal de datos; aplicabilidad de HIPAA u otro; campos exactos de
entidades; preguntas y modelo de evaluación; proveedor de mapas; push en MVP;
integraciones SMS/WhatsApp/email; migración de datos del sistema actual;
fórmulas exactas de impuestos/pensiones/vacaciones/incapacidades/rodamiento;
alcance de facturación. Cada ticket afectado las referencia en sus riesgos.
