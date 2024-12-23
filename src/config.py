import logging
import os

from dotenv import dotenv_values


BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DOTENV_PATH = os.path.join(BASE_DIR, ".env")

if os.path.exists(DOTENV_PATH):
    config = dotenv_values(DOTENV_PATH)
else:
    config = dict()


def env(key):
    return config.get(key)


DEBUG = eval(env("DEBUG"))
BOT_TOKEN = env("BOT_TOKEN")
API_KEY = env("API_KEY")

if DEBUG:
    LOGGING_LEVEL = logging.DEBUG
else:
    LOGGING_LEVEL = logging.INFO
