from keyboards import kb_skip
from lexicon import LEXICON_RU
from state import FSMTaskCreate


async def create_update_title_mixin(message, state):
    await state.update_data(title=message.text)
    await message.answer(LEXICON_RU['title_sent'], reply_markup=kb_skip)



async def create_update_description_mixin(message, state):
    if message.text.lower() == "пропустить":
        await state.update_data(description=None)
        await message.delete()
    else:
        await state.update_data(description=message.text)
