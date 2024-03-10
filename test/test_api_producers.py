from models.producer import ProducerModel
from test.test_fixtures import *


@pytest.fixture()
async def producer_entry(client: AsyncClient) -> ProducerModel:
    response = await client.post("/api/producers/", json={"first_name": "John", "last_name": "Doe"})
    body = response.json()

    assert response.status_code == 200
    assert body["first_name"] == "John"
    assert body["last_name"] == "Doe"

    return body


async def test_list_producers(client: AsyncClient, producer_entry: ProducerModel):
    print(producer_entry)
    response = await client.get("/api/producers/")
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 1
    assert body[0]["id"] == producer_entry["id"]
    assert body[0]["first_name"] == producer_entry["first_name"]
    assert body[0]["last_name"] == producer_entry["last_name"]


async def test_get_producer(client: AsyncClient, producer_entry: ProducerModel):
    response = await client.get(f"/api/producers/{producer_entry['id']}")
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == producer_entry["id"]
    assert body["first_name"] == producer_entry["first_name"]
    assert body["last_name"] == producer_entry["last_name"]


async def test_patch_producer(client: AsyncClient, producer_entry: ProducerModel):
    response = await client.patch(f"/api/producers/{producer_entry['id']}", json={"first_name": "Mister"})
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == producer_entry["id"]
    assert body["first_name"] == "Mister"
    assert body["last_name"] == producer_entry["last_name"]


async def test_override_producer(client: AsyncClient, producer_entry: ProducerModel):
    response = await client.patch(f"/api/producers/{producer_entry['id']}", json={
        "first_name": "Mister",
        "last_name": "Beast"
    })
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == producer_entry["id"]
    assert body["first_name"] == "Mister"
    assert body["last_name"] == "Beast"


async def test_delete_producer(client: AsyncClient, producer_entry: ProducerModel):
    response = await client.get(f"/api/producers/{producer_entry['id']}")
    assert response.status_code == 200

    response = await client.delete(f"/api/producers/{producer_entry['id']}")
    assert response.status_code == 200

    response = await client.get(f"/api/producers/{producer_entry['id']}")
    assert response.status_code == 404
