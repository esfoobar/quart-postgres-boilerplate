import pytest
from quart import current_app

from my_app.counter_app.models import counter_table


@pytest.mark.asyncio
async def test_initial_response(create_test_client):
    response = await create_test_client.get("/")
    body = await response.get_data()
    assert "Counter: 1" in str(body)


@pytest.mark.asyncio
async def test_second_response(create_test_client, create_test_app):
    # Counter 1
    response = await create_test_client.get("/")
    body = await response.get_data()

    # Counter 2
    response = await create_test_client.get("/")
    body = await response.get_data()
    assert "Counter: 2" in str(body)

    # check on the model itself
    async with create_test_app.app_context():
        conn = current_app.dbc  # type: ignore
        counter_query = counter_table.select()
        result = await conn.fetch_all(counter_query)
        result_row = result[0]
        count = result_row["count"]
        assert count == 2
