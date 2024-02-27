from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.request import get_tasks_list

kbr = ReplyKeyboardRemove()

kb_skip: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Пропустить")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)


async def task_list_kb(user_id) -> InlineKeyboardMarkup:
    task_kb_builder = InlineKeyboardBuilder()
    tasks = await get_tasks_list(user_id)
    for task in tasks:
        task_kb_builder.row(
            InlineKeyboardButton(text=task.title,
                                 callback_data=f"task_{task.id}",
                                 selective=True)
        )
    return task_kb_builder.as_markup()


async def task_menu_kb(task_id):
    task_kb_builder = InlineKeyboardBuilder()
    task_kb_builder.row(
        InlineKeyboardButton(text="Удалить",
                             callback_data=f"del_{task_id}"),
        InlineKeyboardButton(text="Изменить",
                             callback_data=f"update_{task_id}"),
    ).row(InlineKeyboardButton(text="Изменить статус",
                               callback_data=f"status_{task_id}"))
    return task_kb_builder.as_markup()


async def task_status_kb(task_id):
    task_kb_builder = InlineKeyboardBuilder()
    task_kb_builder.row(
        InlineKeyboardButton(text="Выполнено",
                             callback_data=f"done_{task_id}"),
    )
    return task_kb_builder.as_markup()
