import config
from logger import logger
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from enum import Enum

bot = Bot(token=config.token)
dp = Dispatcher(bot)


class Mode(Enum):
    converter = "convert_layout"
    echo = "echo"
    help = "help"


mode = Mode.converter


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    convert_layout_button = types.KeyboardButton("/convert_layout")
    echo_button = types.KeyboardButton("/echo")
    help_button = types.KeyboardButton("/help")
    keyboard.add(help_button, echo_button, convert_layout_button)
    await bot.send_message(message.chat.id, 'clear_schedule', reply_markup=keyboard)
    await message.answer("Привет!\nЯ Эхо-бот!\nОтправь мне любое сообщение, а я тебе обязательно отвечу.", reply_markup=keyboard) #Так как код работает асинхронно, то обязательно пишем await.
    logger.debug(f"User {message.from_user.username} started session")


@dp.message_handler(commands=Mode.converter.value)
async def activate_convert_layout(message: types.Message):
    global mode
    logger.debug(f"User {message.from_user.username} changed mode: from {mode} to {Mode.converter.value}")
    mode = Mode.converter


@dp.message_handler(commands=Mode.echo.value)
async def activate_echo(message: types.Message):
    global mode
    mode = Mode.echo


@dp.message_handler(commands="help")
async def write_help(message: types.Message):
    await message.answer("Этот бот нужен для образовательных целей, внём я учусь создавать разный не очень полезный функционал, например, change_layout меняет раскладку клавиатуры у текста")


def detect_lang(text):
    layout_lang = config.eng_dict
    for symbol in text:
        if symbol.lower() in config.eng_dict.keys():
            layout_lang = config.eng_dict
            break
        elif symbol.lower() in config.rus_dict.keys():
            layout_lang = config.rus_dict
            break
    return layout_lang


def convert_layout(message):
    converted_text = ''.join([detect_lang(message.text).get(symbol, symbol) for symbol in message.text])
    return converted_text


@dp.message_handler(content_types=["text"])
async def process_message(message: types.Message):
    converted_text = convert_layout(message)
    if mode == Mode.converter:
        await message.answer(f"`{converted_text}`", parse_mode="Markdown")
        logger.debug(f"User {message.from_user.username} wrote: {message.text} and recieved {converted_text}")
    elif mode == Mode.echo:
        await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)