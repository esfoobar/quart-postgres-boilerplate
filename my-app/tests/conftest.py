from typing import AsyncGenerator

import pytest
from dynaconf import settings
from quart import Quart
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database
from typing_extensions import Never

from my_app.application import create_app
from my_app.db import metadata


@pytest.fixture(scope="function")
async def create_db() -> AsyncGenerator[dict, Never]:

    if settings.ENV_FOR_DYNACONF == "DEVELOPMENT":
        settings.configure(FORCE_ENV_FOR_DYNACONF="TESTING")

    print("Creating db")
    db_name = settings["DATABASE_NAME"] + "_test"
    db_host = settings["DB_HOST"]
    db_username = settings["DB_USERNAME"]
    db_password = settings["DB_PASSWORD"]

    db_test_uri = "postgresql://%s:%s@%s:5432/%s" % (
        db_username,
        db_password,
        db_host,
        db_name,
    )

    # drop the database if it exists
    if database_exists(db_test_uri):
        drop_database(db_test_uri)

    # create test database
    create_database(db_test_uri)

    yield {
        "DB_TEST_URI": db_test_uri,
    }

    print("Destroying db")

    # create new engine to drop test database
    drop_database(db_test_uri)


@pytest.fixture(scope="function")
async def create_test_app(create_db: dict[str, str]) -> AsyncGenerator[Quart, None]:
    app = await create_app(**create_db)
    app_context = app.app_context()
    await app_context.push()

    # Create engine and create all tables
    engine = create_engine(create_db["DB_TEST_URI"])
    metadata.create_all(engine)

    yield app

    # Clean up
    metadata.drop_all(engine)
    await app_context.pop()


@pytest.fixture(scope="function")
async def create_test_client(create_test_app: Quart) -> AsyncGenerator:
    print("Creating test client")
    async with create_test_app.test_client() as client:
        yield client
