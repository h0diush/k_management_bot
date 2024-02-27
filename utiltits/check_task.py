from functools import wraps

from aiogram.types import CallbackQuery

from database.request import get_current_task_for_user
from lexicon import LEXICON_RU


def check_task_exists(func):
    @wraps(func)
    async def wrapper(callback: CallbackQuery, *args, **kwargs):
        task_id = int(callback.data.split('_')[1])
        task = await get_current_task_for_user(task_id)
        if task:
            return await func(callback, *args, **kwargs)
        else:
            await callback.message.answer(LEXICON_RU['not_task'])

    return wrapper
