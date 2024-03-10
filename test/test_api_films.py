from models.producer import ProducerModel
from test.test_api_producers import producer_entry
from test.test_fixtures import *


@pytest.fixture
async def film_entry(client: AsyncClient, producer_entry: ProducerModel):
    response = await client.post("/api/films/", json={
        "producer_id": producer_entry["id"],
        "title": "A cool film",
        "year": 2022
    })
    body = response.json()

    assert response.status_code == 200
    assert body["producer"]["id"] == producer_entry["id"]
    assert body["title"] == "A cool film"
    assert body["year"] == 2022

    return body, producer_entry


async def test_list_films(client: AsyncClient, film_entry):
    film, producer = film_entry
    response = await client.get("/api/films/")
    body = response.json()

    assert response.status_code == 200
    assert body[0]["id"] == film["id"]
    assert body[0]["title"] == film["title"]
    assert body[0]["year"] == film["year"]
    assert body[0]["producer"]["id"] == producer["id"]
    assert body[0]["producer"]["first_name"] == producer["first_name"]
    assert body[0]["producer"]["last_name"] == producer["last_name"]


async def test_get_film(client: AsyncClient, film_entry):
    film, producer = film_entry
    response = await client.get(f"/api/films/{film['id']}")
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == film["id"]
    assert body["title"] == film["title"]
    assert body["year"] == film["year"]
    assert body["producer"]["id"] == producer["id"]
    assert body["producer"]["first_name"] == producer["first_name"]
    assert body["producer"]["last_name"] == producer["last_name"]


async def test_patch_film(client: AsyncClient, film_entry):
    film, producer = film_entry
    response = await client.patch(f"/api/films/{film['id']}", json={
        "title": "Film 1"
    })
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == film["id"]
    assert body["title"] == "Film 1"
    assert body["year"] == film["year"]
    assert body["producer"]["id"] == producer["id"]


async def test_override_film(client: AsyncClient, film_entry):
    film, producer = film_entry
    response = await client.put(f"/api/films/{film['id']}", json={
        "producer_id": producer["id"],
        "title": "Film 1",
        "year": 1998
    })
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == film["id"]
    assert body["title"] == "Film 1"
    assert body["year"] == 1998
    assert body["producer"]["id"] == producer["id"]


async def test_delete_film(client: AsyncClient, film_entry):
    film, _ = film_entry
    response = await client.get(f"/api/films/{film['id']}")
    assert response.status_code == 200

    response = await client.delete(f"/api/films/{film['id']}")
    assert response.status_code == 200

    response = await client.get(f"/api/films/{film['id']}")
    assert response.status_code == 404
