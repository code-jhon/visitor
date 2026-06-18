# VIS-2 — Autenticación, autorización RBAC y gestión de usuarios/roles

| Campo | Valor |
|---|---|
| Ticket | [VIS-2](https://linear.app/parrot-apps/issue/VIS-2/vis-2-autenticacion-autorizacion-rbac-y-gestion-de-usuariosroles) |
| Estado | Backlog |
| Prioridad | Urgent |
| Labels | ninguna |
| Rama sugerida | `feature/VIS-2` |
| Estrategia generada | 2026-06-18 |

> Lee primero `docs/tickets/_ARQUITECTURA.md`. Proyecto nuevo: rutas a crear.

## 1. Contexto y objetivo
Capa de seguridad sobre la que opera todo el sistema: login seguro, control de acceso basado en roles (RBAC) y gestión de usuarios, roles y perfiles. Cada endpoint y vista posterior dependerá de los permisos definidos aquí.

## 2. Alcance
- **Incluye:** login y gestión de sesión/tokens (JWT); RBAC con verificación de permisos en todas las APIs; recuperación de contraseña; hash seguro; CRUD de usuarios; asignación de roles; perfiles por rol (empleado, cliente/paciente, proveedor/coordinador, soporte); activar/desactivar cuentas.
- **No incluye:** MFA (futuro, opcional); registro de auditoría detallado (VIS-4, aunque aquí se emiten los eventos de auth).

## 3. Análisis técnico
Backend (`apps/api`): implementar en `app/core/security.py` (hashing con passlib/bcrypt, emisión/verificación de JWT) y `app/core/permissions.py` (dependencia FastAPI que valida rol/permiso por endpoint). Routers en `app/api/routers/auth.py` y `app/api/routers/users.py`. Modelos `User`, `Role`, `Permission` y perfiles en `app/db/models` (coordinar con VIS-3, que define el modelo completo: aquí se crean estas tablas concretas). Web/móvil: pantallas de login, almacenamiento seguro de token (SecureStore en móvil, httpOnly/secure en web), interceptores que adjuntan el token y refrescan sesión.

## 4. Plan de implementación
1. Modelos `User`, `Role`, `Permission`, tablas de perfil por rol; migración Alembic.
2. `app/core/security.py`: hashing de contraseñas, creación y verificación de access/refresh tokens.
3. `app/core/permissions.py`: dependencia `require_roles(...)`/`require_permission(...)` reutilizable.
4. Router `auth`: `POST /auth/login`, `POST /auth/refresh`, `POST /auth/password-reset/request`, `POST /auth/password-reset/confirm`.
5. Router `users`: CRUD de usuarios, asignación de roles, activar/desactivar.
6. Aplicar la dependencia de permisos como patrón estándar para el resto de routers.
7. Web: pantalla de login, manejo de sesión en `src/store`, cliente HTTP en `src/api` con interceptor.
8. Móvil: pantalla de login, almacenamiento seguro de token, interceptor equivalente.

## 5. Datos y migraciones
Crea tablas `user`, `role`, `permission`, relación rol-permiso y tablas de perfil por rol. Seed inicial de roles del PRD §4 (Admin, Empresa, Empleado, Proveedor/Coordinador, Cliente, Soporte) y un usuario Admin.

## 6. i18n
Claves para pantallas de login, errores de autenticación y recuperación de contraseña (idioma base inglés).

## 7. Criterios de aceptación
- Los usuarios solo acceden a recursos permitidos por su rol/permiso.
- Las solicitudes no autorizadas se rechazan (401/403).
- Los eventos de autenticación quedan disponibles para auditoría (VIS-4).
- Los cambios de cuenta se reflejan en web y móvil.
- Los usuarios desactivados no pueden iniciar sesión.

## 8. Pruebas y verificación
Probar login válido/ inválido, refresh, expiración de token, recuperación de contraseña, acceso denegado por rol, y desactivación de cuenta. Verificar que un endpoint protegido rechaza sin token.

## 9. Riesgos y consideraciones
Definir bien la matriz rol→permiso (insumo de todos los módulos). El país/marco legal (PRD §14) puede exigir controles adicionales. Política de expiración/refresh de tokens y almacenamiento seguro en móvil.

## 10. Dependencias
Bloqueado por VIS-1. **Bloquea** prácticamente todos los módulos funcionales (VIS-4, VIS-5, VIS-18, etc.).
