from dotenv import load_dotenv
import os
load_dotenv()

class Environments:
    dev = 'dev'
    test = 'test'

class Config(object):
    ENV = 'dev'


class DevelopmentConfig(Config):
    DATABASE_NAME = os.getenv('DEV__DATABASE_NAME', 'dev')

class TestingConfig(Config):
    DATABASE_NAME = os.getenv('TEST__DATABASE_NAME', 'test')


class StagingConfig(Config):
    pass


class ProductionConfig(Config):
    pass

def get_current_config():
    env = os.getenv('ENV', 'dev')
    if env == Environments.dev:
        return DevelopmentConfig
    if env == Environments.test:
        return TestingConfig