import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(__file__)

# TODO: 나중에 ENV 파일로 대체 => 현재는 None이라고만 인식됨
user = 'dolly' # os.getenv('PG_USER')
password = '--' # os.getenv('PG_PASSWORD')
host = 'localhost' # os.getenv('PG_HOST')
database = 'pybodb' # os.getenv('PG_DB')
port = 5432 # os.getenv('PG_PORT')

# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
print(SQLALCHEMY_DATABASE_URI)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# secret key 추가
SECRET_KEY = "dev"


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "production": ProductionConfig
}