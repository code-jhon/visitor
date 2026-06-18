"""SQLAlchemy models (VIS-2 introduces auth/RBAC tables).

VIS-3 extends this package with the full domain model. Models are imported
here so Alembic's autogenerate and ``Base.metadata`` see them.
"""
from app.db.models.user import (
    Permission,
    Role,
    User,
    UserProfile,
    role_permissions,
    user_roles,
)

__all__ = [
    "User",
    "Role",
    "Permission",
    "UserProfile",
    "user_roles",
    "role_permissions",
]
