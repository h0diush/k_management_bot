from aiogram.fsm.state import State, StatesGroup


class FSMTaskCreate(StatesGroup):
    title = State()
    description = State()


class FSMTaskUpdate(StatesGroup):
    title = State()
    description = State()
    task_id = State()
