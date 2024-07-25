import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('PG_USER')
password = os.getenv('PG_PASSWORD')
host = os.getenv('PG_HOST')
database = os.getenv('PG_DB')
port = os.getenv('PG_PORT')

print("PG_USER:", os.getenv('PG_USER'))
print("PG_PASSWORD:", os.getenv('PG_PASSWORD'))
print("PG_HOST:", os.getenv('PG_HOST'))
print("PG_DB:", os.getenv('PG_DB'))
print("PG_PORT:", os.getenv('PG_PORT'))
print(os.getenv("CONFIG_MODE", "development"))
SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
print(SQLALCHEMY_DATABASE_URI)
