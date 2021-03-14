import random
from faker import Faker
from models import Audio, AudioTypes, BaseMetadata, AudioBookMetadata, SongMetadata, PodcastMetadata


faker = Faker()

class AudioFactory:
    def __init__(
        self,
        audio_type=random.choice([AudioTypes.audio_book, AudioTypes.podcast, AudioTypes.song]),
        name = faker.name()[:100],
        duration = random.randint(1, 30000),
        uploaded_time = faker.date_time(),
        host = faker.name()[:100],
        author = faker.name()[:100],
        narrator = faker.name()[:100],
        participants = [faker.name()[:100] for participants in range(random.randint(1, 100))]
    ):
        self.audio_type = audio_type
        self.name = name
        self.duration = duration
        self.uploaded_time = uploaded_time
        self.host = host
        self.author = author
        self.narrator = narrator
        self.participants = participants

    def build(self):
        metadata: Union[AudioBookMetadata, PodcastMetadata, SongMetadata]
        base_metadata_dict = BaseMetadata(
            name=self.name,
            duration=self.duration,
            uploaded_time=self.uploaded_time
        ).dict()
        if self.audio_type == AudioTypes.audio_book:
            metadata = AudioBookMetadata(
                author=self.author,
                narrator=self.narrator,
                **base_metadata_dict
            )
        elif self.audio_type == AudioTypes.podcast:
            metadata = PodcastMetadata(
                host=self.host,
                participants=self.participants,
                **base_metadata_dict
            )
        else:
            metadata = SongMetadata(**base_metadata_dict)
        audio = Audio(audio_type=self.audio_type, metadata=metadata)
        return audio

if __name__ == '__main__':
    print(AudioFactory().build())