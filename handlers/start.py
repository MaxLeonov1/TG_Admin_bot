import os
from idlelib.undo import Command
from aiogram.filters import Command
from aiogram import F
from aiogram.types import Message
from loader import  router, bot

@router.message(Command('start'))
async def start_message(message: Message):
    await message.answer("Привет! Я бот администратор")