from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from database.request import get_current_task_for_user, delete_current_task, \
    insert_task, update_current_task, update_status_task
from keyboards import task_list_kb, task_menu_kb, kbr, task_status_kb
from lexicon import LEXICON_RU
from models.models import StatusTask
from state import FSMTaskCreate, FSMTaskUpdate
from utiltits import create_update_title_mixin, \
    create_update_description_mixin, check_task_exists

task_commands_router = Router()


@task_commands_router.message(Command(commands='cancel'),
                              StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(LEXICON_RU['cancel_out_form_task'])


@task_commands_router.message(Command(commands='cancel'),
                              ~StateFilter(default_state))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(LEXICON_RU[message.text])
    await state.clear()


@task_commands_router.message(Command(commands="create_task"),
                              StateFilter(default_state))
async def process_create_task_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU[message.text])
    await state.set_state(FSMTaskCreate.title)


@task_commands_router.message(StateFilter(FSMTaskCreate.title), F.text != '')
async def process_title_sent(message: Message, state: FSMContext):
    await create_update_title_mixin(message=message, state=state)
    await state.set_state(FSMTaskCreate.description)


@task_commands_router.message(StateFilter(FSMTaskCreate.title))
async def warning_not_title(message: Message):
    await message.answer(LEXICON_RU['warning_title'])


@task_commands_router.message(StateFilter(FSMTaskCreate.description),
                              F.text != '')
async def process_description_sent(message: Message, state: FSMContext):
    await create_update_description_mixin(message=message, state=state)
    data = await state.get_data()
    await insert_task(title=data["title"], description=data["description"],
                      user_id=message.from_user.id)
    await state.clear()
    await message.answer(LEXICON_RU['description_sent'], reply_markup=kbr)


@task_commands_router.message(StateFilter(FSMTaskCreate.description))
async def warning_not_description(message: Message):
    await message.answer(LEXICON_RU['warning_description'])


@task_commands_router.message(Command(commands='tasks'))
async def process_my_task_command(message: Message):
    await message.answer(
        text=LEXICON_RU[message.text],
        reply_markup=await task_list_kb(message.from_user.id)
    )


@task_commands_router.callback_query(F.data.startswith('task_'))
@check_task_exists
async def get_current_task(callback: CallbackQuery):
    task_id = callback.data.split('_')[1]
    task = await get_current_task_for_user(task_id=int(task_id))
    await callback.message.answer(
        f"{task.title}\n\n{task.description if task.description else ''}"
        f"\nСоздано: {task.created_at.strftime('%H:%M %d.%m.%Y')}"
        f"\n<b>Статус: {task.status.value}</b>",
        reply_markup=await task_menu_kb(task_id)
    )


@task_commands_router.callback_query(F.data.startswith("del_"))
@check_task_exists
async def process_delete_task(callback: CallbackQuery):
    task_id = callback.data.split('_')[1]
    await delete_current_task(int(task_id))
    await callback.message.answer(text=LEXICON_RU['task_del'])


@task_commands_router.callback_query(F.data.startswith('update_'))
@check_task_exists
async def process_update_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON_RU['start_update_task'])
    task_id = int(callback.data.split('_')[1])
    await state.set_state(FSMTaskUpdate.title)
    await state.update_data(task_id=task_id)


@task_commands_router.message(StateFilter(FSMTaskUpdate.title))
async def process_update_title(message: Message, state: FSMContext):
    await create_update_title_mixin(message=message, state=state)
    await state.set_state(FSMTaskUpdate.description)


@task_commands_router.message(StateFilter(FSMTaskUpdate.description))
async def process_update_description(message: Message, state: FSMContext):
    await create_update_description_mixin(message=message, state=state)
    data = await state.get_data()
    await update_current_task(title=data['title'],
                              description=data['description'],
                              task_id=data['task_id'])
    await state.clear()
    await message.answer(LEXICON_RU['update_task_sent'])


@task_commands_router.callback_query(F.data.startswith('status_'))
@check_task_exists
async def process_status_command(callback: CallbackQuery):
    task_id = int(callback.data.split('_')[1])
    task = await get_current_task_for_user(task_id)
    if task.status == StatusTask.done:
        await callback.message.answer(LEXICON_RU['task_with_completed_status'])
    else:
        await callback.message.answer(f'{task.title} - {task.status.value}',
                                      reply_markup=await task_status_kb(
                                          task_id))


@task_commands_router.callback_query(F.data.startswith('done_'))
async def process_status_done_command(callback: CallbackQuery):
    task_id = int(callback.data.split('_')[1])
    await update_status_task(status=StatusTask.done, task_id=task_id)
    await callback.message.answer(LEXICON_RU['status_done_complied'])
