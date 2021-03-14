import json
import pytest
from main import app
from fastapi import HTTPException
from httpx import AsyncClient
from fastapi.testclient import TestClient
from odmantic.bson import ObjectId
from factory import AudioFactory
from models import Audio, AUDIO_TYPES

# client = TestClient(app)

@pytest.mark.asyncio
async def test_get_list():
    TEST_LENGTH = 10
    for audio_type in AUDIO_TYPES:
        [AudioFactory().build().save() for a in range(TEST_LENGTH)]
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"/{audio_type}")
            assert response.status_code == 200
            data = response.json()
            assert len(data) >= TEST_LENGTH

@pytest.mark.asyncio
async def test_create_item():
    data = AudioFactory().build()
    request_data = json.loads(data.json())
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/", json=request_data)
        assert response.status_code == 200
        audio_id = ObjectId(response.json()['id'])
        # import pudb; pudb.set_trace()
        created_audio = await Audio.find_by_id(data.audio_type, audio_id)
        created_audio_json = json.loads(created_audio.json())
        assert created_audio
        for key in request_data.keys():
            if key == 'id':
                continue
            assert request_data[key] == created_audio_json[key]


@pytest.mark.asyncio
async def test_get_item():
    data = AudioFactory().build()
    await data.save()
    request_data = json.loads(data.json())
    async with AsyncClient(app=app, base_url="http://test") as ac:
        path = f"/{data.audio_type}/{data.metadata.id}"
        response = await ac.get(path)
        assert response.status_code == 200
        audio_id = ObjectId(response.json()['id'])
        created_audio = await Audio.find_by_id(data.audio_type, audio_id)
        assert created_audio
        created_audio_json = json.loads(created_audio.json())
        for key in request_data.keys():
            assert request_data[key] == created_audio_json[key]


@pytest.mark.asyncio
async def test_delete_item():
    data = AudioFactory().build()
    await data.save()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        path = f"/{data.audio_type}/{data.metadata.id}"
        response = await ac.delete(path)
        assert response.status_code == 200
        with pytest.raises(HTTPException):
            await Audio.find_by_id(data.audio_type, data.metadata.id)

@pytest.mark.asyncio
async def test_create_item():
    data = AudioFactory().build()
    await data.save()
    request_data = json.loads(AudioFactory().build().json())
    async with AsyncClient(app=app, base_url="http://test") as ac:
        path = f"/{data.audio_type}/{data.metadata.id}"
        response = await ac.post(path, json=request_data)
        updated_audio = await Audio.find_by_id(data.audio_type, data.metadata.id)
        assert response.status_code == 200
        updated_audio = await Audio.find_by_id(data.audio_type, data.metadata.id)
        updated_audio_json = json.loads(updated_audio.json())
        for key in request_data.keys():
            if key == 'id':
                continue
            assert request_data[key] == updated_audio_json[key]