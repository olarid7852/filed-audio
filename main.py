from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, PositiveInt
from models import Audio, AudioTypes, AudioBookMetadata, SongMetadata, PodcastMetadata, BaseMetadata
from odmantic import AIOEngine, Model, bson

from db import engine

app = FastAPI()

@app.get("/{audio_type}/{audio_id}")
async def get_audio(audio_type: AudioTypes, audio_id: bson.ObjectId):
    return await Audio.find_by_id(audio_type, audio_id)

@app.get("/{audio_type}")
async def list_audios(audio_type: AudioTypes):
    return await Audio.find_all(audio_type)

@app.post("/")
async def create_audio(item: Audio):
    return await item.save()

@app.post("/{audio_type}/{audio_id}")
async def update_audio(audio_type: AudioTypes, audio_id: bson.ObjectId, item: Audio):
    audio = await Audio.find_by_id(audio_type, audio_id)
    await audio.update(item)
    return {'status': True}

@app.delete("/{audio_type}/{audio_id}")
async def delete_audio(audio_type: AudioTypes, audio_id: bson.ObjectId):
    await Audio.delete_audio(audio_type, audio_id)
    return {'status': True}