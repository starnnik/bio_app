from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from sqlalchemy import create_engine

from app.core.database import Base


def _config(url: str) -> Config:
    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", url)
    return cfg


def test_migrations_match_models(tmp_path, monkeypatch):
    db = tmp_path / "m.db"
    monkeypatch.setattr("app.core.config.settings.database_url", f"sqlite+aiosqlite:///{db}")
    cfg = _config(f"sqlite+aiosqlite:///{db}")

    # env.py runs asyncio.run itself, so call it from a plain (non-async) test.
    command.upgrade(cfg, "head")

    engine = create_engine(f"sqlite:///{db}")
    with engine.connect() as conn:
        diff = compare_metadata(MigrationContext.configure(conn), Base.metadata)
    assert diff == []

    command.downgrade(cfg, "base")
