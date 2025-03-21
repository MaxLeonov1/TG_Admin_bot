from aiogram import Bot, Dispatcher, Router
from aiohttp.web_routedef import route

from config.config import TOKEN


router = Router()
dp = Dispatcher()
dp.include_router(router)
bot = Bot(TOKEN)

#список запрещенных слов
FORBIDDEN_WORDS = [
    'спам',
    'реклама',
    'взлом',
]

#Хранилище данных о нарушениях
user_violations = {}
# Число нарушений до блокировки
MAX_VIOLATIONS = 3
# Длительность блокировки
MUTE_DURATION = 10
