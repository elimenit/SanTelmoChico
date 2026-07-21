"""Constantes o variabes que vienen del entorno virtual. 
"""
from dotenv import load_dotenv
import os

load_dotenv()
# JWT
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

# PostgreSQL
FIRST_SUPERUSER_EMAIL = os.getenv('FIRST_SUPERUSER_EMAIL')
FIRST_SUPERUSER_PASSWORD = os.getenv('FIRST_SUPERUSER_PASSWORD')
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
NAME_DB = os.getenv('NAME_DB')

# Redis
SERVER_REDIS = os.getenv('SERVER_REDIS')
PORT_REDIS = os.getenv('PORT_REDIS')

# Kafka
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID')
# Email
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def validate_constants(value, name: str):
    if not value:
        raise ValueError(f"Falta estabecer la variable de entorno: {name}")