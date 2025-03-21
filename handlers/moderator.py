from aiogram.types import Message
from loader import (router, user_violations, MAX_VIOLATIONS, MUTE_DURATION, FORBIDDEN_WORDS)
from datetime import timedelta, datetime

async def record_violatation(user_id):
    if user_id not in user_violations:
        user_violations[user_id] = {
            'count': 0,
            'last_violation': None
        }
    violations = user_violations[user_id]
    violations['count'] += 1
    violations['last_violation'] = datetime.now()

async def check_user_mute(user_id):
    if user_id in user_violations:
        violations = user_violations[user_id]
        if violations['count'] >= MAX_VIOLATIONS:
            mute_end = violations['last_violation'] + timedelta(minutes=MUTE_DURATION)
            if datetime.now() < mute_end:
                return True
            else:
                user_violations[user_id] = {'count': 0, 'last_violation': None}
    return False

@router.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    if await check_user_mute(user_id):
        await message.delete()
        try:
            await message.answer(
                f"@{message.from_user.username}, вы временно ограничены"
                f"в отправке сообщений на {MUTE_DURATION} минут из-за частых нарушений.")
            return
        except:
            await message.answer(
                f"{message.from_user.first_name} {message.from_user.last_name},вы временно ограничены"
                f"в отправке сообщений на {MUTE_DURATION} минут из-за частых нарушений.")
            return
    if message.entities:
        for entity in message.entities:
            if entity.type in ['url','text_link']:
                await message.delete()
                await record_violatation(user_id)
                try:
                    await message.answer(
                        f"@{message.from_user.username}, сообщение удалено: "
                        f"содержит ссылку. Нарушение #{user_violations[user_id]['count']}")
                    return
                except:
                    await message.answer(
                        f"{message.from_user.first_name} {message.from_user.last_name},сообщение удалено: "
                        f"содержит ссылку. Нарушение #{user_violations[user_id]['count']}")
                    return
    text = message.text.lower()
    for word in FORBIDDEN_WORDS:
        if word in text:
                await message.delete()
                await record_violatation(user_id)
                try:
                    await message.answer(
                        f"@{message.from_user.username}, сообщение удалено: "
                        f"содержит запрещенное слово. Нарушение #{user_violations[user_id]['count']}")
                    return
                except:
                    await message.answer(
                        f"{message.from_user.first_name} {message.from_user.last_name},сообщение удалено: "
                        f"содержит запрещенное слово. Нарушение #{user_violations[user_id]['count']}")
                    return