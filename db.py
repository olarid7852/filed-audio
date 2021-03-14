from odmantic import AIOEngine, Model, bson
from config import get_current_config

config = get_current_config()
engine = AIOEngine(database=config.DATABASE_NAME)