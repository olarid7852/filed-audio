import json
import pytest
# from unittest.mock import AsyncMock,patch
from typing import Union
from factory import AudioFactory
from models import Audio, AudioTypes


@pytest.mark.asyncio
async def test_unsaved_data():
    audio = AudioFactory().build()
    with pytest.raises(Exception):
        await Audio.find_by_id(audio.audio_type, audio.metadata.id)

@pytest.mark.asyncio
async def test_save_and_find_audio():
    audio = AudioFactory().build()
    await audio.save()

def test_reject_empty_data():
    with pytest.raises(ValueError):
        audio = Audio(**{})

def test_correct_audio():
    audio = None
    audio = AudioFactory().build().dict()
    assert Audio(**audio)

def test_reject_audio_type_support():
    with pytest.raises(ValueError):
        audio = AudioFactory().build()
        audio = Audio(audio_type='a', metadata=audio.metadata)

@pytest.mark.asyncio
async def test_save():
    audio = AudioFactory().build()
    await audio.save()
    audio = await Audio.find_by_id(audio.audio_type, audio.metadata.id)
    assert audio

@pytest.mark.asyncio
async def test_delete_audio():
    audio = AudioFactory().build()
    await audio.save()
    await Audio.delete_audio(audio.audio_type, audio.metadata.id)
    with pytest.raises(Exception):
        audio = await Audio.find_by_id(audio.audio_type, audio.metadata.id)


@pytest.mark.asyncio
async def test_update_audio():
    audio = AudioFactory().build()
    await audio.save()
    test_update_audio_data = AudioFactory(audio_type=audio.audio_type).build()
    await audio.update(test_update_audio_data)
    updated_audio = await Audio.find_by_id(audio.audio_type, audio.metadata.id)
    test_update_audio_data_dict = json.loads(test_update_audio_data.json())
    updated_audio_dict = json.loads(audio.json())
    for key in updated_audio_dict.keys():
        if key == 'id':
            continue
        assert updated_audio_dict[key] == test_update_audio_data_dict[key]