from typing import Any, AsyncGenerator

import pytest
from dynaconf import settings
from quart import Quart
from sqlalchemy import create_engine

from my_app.application import create_app
from my_app.db import metadata


@pytest.fixture
async def create_db() -> Any:
    print("Creating db")
    db_name = settings["DATABASE_NAME"]
    db_host = settings["DB_HOST"]
    db_username = settings["DB_USERNAME"]
    db_password = settings["DB_PASSWORD"]

    db_uri = "postgresql://%s:%s@%s:5432/" % (
        db_username,
        db_password,
        db_host,
    )

    engine = create_engine(db_uri + db_name)
    conn = engine.connect()

    db_test_name = settings["DATABASE_NAME"] + "_test"

    # drop database if exists from previous run
    try:
        conn.execute("COMMIT")
        conn.execute(f"DROP DATABASE {db_test_name} WITH (FORCE)")
    except:
        pass

    conn.execute("COMMIT")
    conn.execute("CREATE DATABASE " + db_test_name)
    conn.close()

    print("Creating test tables")
    engine = create_engine(db_uri + db_test_name)
    metadata.bind = engine
    metadata.create_all()

    yield {
        "DB_USERNAME": db_username,
        "DB_PASSWORD": db_password,
        "DB_HOST": db_host,
        "DATABASE_NAME": db_test_name,
        "DB_URI": db_uri + db_test_name,
        "TESTING": True,
    }

    print("Destroying db")
    engine = create_engine(db_uri + db_name)
    conn = engine.connect()

    conn.execute("COMMIT")
    conn.execute(f"DROP DATABASE {db_test_name} WITH (FORCE)")
    conn.close()


@pytest.fixture
async def create_test_app(create_db) -> Any:
    app = create_app(**create_db)
    await app.startup()
    yield app
    await app.shutdown()


@pytest.fixture
def create_test_client(create_test_app) -> Any:
    print("Creating test client")
    return create_test_app.test_client()
