from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv

# Абсолютный путь к текущей директории
BASE_DIR = Path(__file__).resolve().parent

"load_dotenv(BASE_DIR / '.env')")

@dataclass(frozen=True)
class Settings:
    bot_token: str

def get_settings():
    token=os.getenv('BOT_TOKEN')
    if not token:
        raise RuntimeError("Не найден токен бота.Создайте его в .env файле")
    return Settings(bot_token=token)