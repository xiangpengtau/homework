from logging.config import fileConfig

from alembic.script import ScriptDirectory
from alembic import context
from sqlmodel import SQLModel
from sqlalchemy import inspect

from app.core.db_config import DB_ENGINE, DB_URI
from app.db.models import *

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def create_tables_if_not_exist():
    """Directly create tables that don't exist"""
    inspector = inspect(DB_ENGINE)
    existing_tables = inspector.get_table_names()

    # Get all tables defined in models
    defined_tables = SQLModel.metadata.tables

    # Create tables that don't exist
    for table_name, table in defined_tables.items():
        if table_name not in existing_tables:
            print(f"Creating table: {table_name}")
            table.create(DB_ENGINE)
        else:
            print(f"Table {table_name} already exists")


def process_revision_directives(context, revision, directives) -> None:  # type: ignore
    if config.cmd_opts and config.cmd_opts.autogenerate:
        script = directives[0]

        if script.upgrade_ops.is_empty():
            directives[:] = []
            print("No changes detected.")
        else:
            head_revision = ScriptDirectory.from_config(config).get_current_head()

            if head_revision is None:
                new_rev_id = 1
            else:
                last_rev_id = int(head_revision.lstrip("0"))
                new_rev_id = last_rev_id + 1
            script.rev_id = "{0:04}".format(new_rev_id)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    try:
        # First try to create tables directly
        create_tables_if_not_exist()
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
        print("Falling back to migrations...")

        # If table creation fails, proceed with normal migration process
        with DB_ENGINE.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                process_revision_directives=process_revision_directives,
                compare_type=True,
                dialect_opts={"paramstyle": "named"},
            )

            with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

# If you want to create tables directly when executing this file, add this condition
if __name__ == "__main__":
    create_tables_if_not_exist()
