from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, User, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Format, List, Multi, Const, Case
from aiogram_dialog.widgets.kbd import Button, Row
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

router = Router()


class StartSG(StatesGroup):
    start = State()


# Это хэндлер, обрабатывающий нажатие инлайн-кнопок
async def button_clicked(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    another_button = dialog_manager.dialog_data.get('another_button')
    dialog_manager.dialog_data.update(another_button=not another_button)


# Это геттер
async def get_button_status(dialog_manager: DialogManager, **kwargs):
    another_button = dialog_manager.dialog_data.get('another_button')
    return {'button_status': another_button}

window = Window(
    Const('Это сообщение с инлайн-кнопками'),
    Row(
        Button(text=Const('1'), id='button_1'),
        Button(text=Const('2'), id='button_2'),
        Button(text=Const('3'), id='button_3'),
        Button(text=Const('4'), id='button_4'),
        Button(text=Const('5'), id='button_5'),
        Button(text=Const('6'), id='button_6'),
        Button(text=Const('7'), id='button_7'),
        Button(text=Const('8'), id='button_8'),
        Button(text=Const('9'), id='button_9'),
    ),
    state=StartSG.start
)

start_dialog = Dialog(window)


# Это классический хэндлер на команду /start
@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


dp.include_router(router)
dp.include_router(start_dialog)
setup_dialogs(dp)
dp.run_polling(bot)
