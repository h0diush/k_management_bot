from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from lexicon import LEXICON_RU

base_command_router = Router()


@base_command_router.message(CommandStart())
async def process_command_start(message: Message):
    await message.answer(LEXICON_RU[message.text])


@base_command_router.message(Command(commands='help'))
async def process_command_help(message: Message):
    await message.answer(LEXICON_RU[message.text])
