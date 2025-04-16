import os
from dotenv import load_dotenv

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("API_KEY")
OPENAI_MODEL = os.getenv("MODEL")
OPENAI_BASE_URL = os.getenv("BASE_URL")

DS_API_KEY = os.getenv("DS_API_KEY")
DS_MODEL = os.getenv("DS_MODEL")
DS_BASE_URL = os.getenv("DS_BASE_URL")

DB_PATH = os.getenv("DB_PATH")
