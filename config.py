import os

import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_TG_ID = int(os.getenv('ADMIN_TG_ID'))
CHANNEL_URL = os.getenv('CHANNEL_URL')

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

REFERRAL_LINK_BASE = 'https://t.me/stone_referral_bot?start='

SLIDESHOW_TASK = None
