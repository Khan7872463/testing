import os
import logging
from logging.handlers import RotatingFileHandler


BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
APP_ID = int(os.environ.get("APP_ID", ""))
API_HASH = os.environ.get("API_HASH", "")
BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))
PORT = os.environ.get("PORT", "8080")
auth_token = os.environ.get("AUTH_TOKEN","zrmZ1fem9erEK%2BbBQpSqldBcP0HJ8PxyIbDw3HWlCfiGe4kI3MVGq4tK6OGC3s0WdIqPGRP5FvmMsQvQWe8t6g%3D%3D")
gogoanime_token = os.environ.get("GOGOANIME_TOKEN","58p11ds5010l3vbuoh9v46bm72")

# Logger configuration
LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
