# migrations/env.py
from __future__ import annotations

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# --- Alembic base config ---
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Cargar tu app Flask y metadata de modelos ---
# Asegura que 'app/' esté importable (si ejecutas desde la raíz del repo, no hace falta)
# import sys; sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # opcional

from app import create_app
from app.extensions import db

# Inicializa la app y registra modelos en el metadata
flask_app = create_app()
flask_app.app_context().push()

# Lee DATABASE_URL del entorno y la inyecta en alembic.ini
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# Metadata que usará Alembic para autogenerate
target_metadata = db.metadata


def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo 'offline' (sin crear Engine)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,               # detecta cambios de tipo
        compare_server_default=True,     # detecta defaults en server
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta migraciones en modo 'online' (con Engine y conexión)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            render_as_batch=False,  # True solo si migras SQLite con alter de columnas
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
