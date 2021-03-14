from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel, Field, PositiveInt, constr, validator
from odmantic import Model, bson
from typing import List, Optional, Union
from enum import Enum, IntEnum
from db import engine

Audio = None
class AudioTypes(str, Enum):
    song = 'song'
    audio_book = 'audio_book'
    podcast = 'podcast'

AUDIO_TYPES = [AudioTypes.audio_book, AudioTypes.podcast, AudioTypes.song]

class BaseMetadata(BaseModel):
    duration: PositiveInt
    name: constr(max_length=100)
    uploaded_time: datetime

    audio_type: AudioTypes = AudioTypes.song

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        if data.get('id'):
            del(data['id'])
        if(data.get('audio_type')):
            del(data['audio_type'])
        return data


class SongMetadata(Model, BaseMetadata):
    # audio_type: AudioTypes = AudioTypes.song

    duration: PositiveInt
    name: constr(max_length=100)
    uploaded_time: datetime

    @property
    def audio_type(self):
        return AudioTypes.song


class PodcastMetadata(Model, BaseMetadata):
    # audio_type: AudioTypes = AudioTypes.podcast

    duration: PositiveInt
    name: constr(max_length=100)
    uploaded_time: datetime
    
    host: constr(max_length=100)
    participants: List[constr(max_length=100)]

    @property
    def audio_type(self):
        return AudioTypes.podcast


class AudioBookMetadata(Model, BaseMetadata):
    # audio_type: AudioTypes = AudioTypes.audio_book

    duration: PositiveInt
    name: constr(max_length=100)
    uploaded_time: datetime

    author: constr(max_length=100)
    narrator: constr(max_length=100)

    @property
    def audio_type(self):
        return AudioTypes.audio_book



class Audio(BaseModel):
    audio_type: AudioTypes
    metadata: Union[AudioBookMetadata, PodcastMetadata, SongMetadata,]

    @validator('metadata', pre=True)
    def metadata_must_be_based_on_type(cls, v, values):
        if type(v) != dict:
            return v
        audio_type: AudioTypes = values.get('audio_type')
        if audio_type == AudioTypes.podcast:
            # import pudb; pudb.set_trace()
            return PodcastMetadata(**v)
        if audio_type == AudioTypes.audio_book:
            # import pudb; pudb.set_trace()
            return AudioBookMetadata(**v)
        if audio_type == AudioTypes.song:
            return SongMetadata(**v)
        else:
            raise ValueError("Invalid Type")
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()
    
    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        if self.metadata.id:
            data['id'] = str(self.metadata.id)
        return data

    async def update(self, item: Audio):
        item_dict = item.metadata.dict(exclude_unset=True)
        for name, value in item_dict.items():
            if name == 'id':
                continue
            setattr(self.metadata, name, value)
        await engine.save(self.metadata)
    
    async def save(self):
        self.metadata = await engine.save(self.metadata)
        return self
    
    @staticmethod
    def _get_metadata_class(audio_type: AudioTypes):
        if audio_type == audio_type.audio_book:
            return AudioBookMetadata, AudioBookMetadata.id
        if audio_type == AudioTypes.song:
            return SongMetadata, SongMetadata.id
        if audio_type == AudioTypes.podcast:
            return PodcastMetadata, SongMetadata.id

    @staticmethod
    async def find_all(audio_type: AudioTypes):
        model_class = Audio._get_metadata_class(audio_type)[0]
        return [Audio(metadata=audio, audio_type=audio_type) for audio in await engine.find(model_class)]
    
    @staticmethod
    async def find_by_id(audio_type: AudioTypes, audio_id: bson.ObjectId):
        model_class, id_element = Audio._get_metadata_class(audio_type)
        audio = await engine.find_one(model_class, id_element == audio_id)
        if not audio:
            raise HTTPException(status_code=404, detail='object not found')
        return Audio(metadata=audio, audio_type=audio_type)
    
    @staticmethod
    async def delete_audio(audio_type: AudioTypes, audio_id: bson.ObjectId):
        audio = await Audio.find_by_id(audio_type, audio_id)
        await engine.delete(audio.metadata)
        