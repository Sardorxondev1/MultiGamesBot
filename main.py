from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle, ChosenInlineResult
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Filter
import asyncio, os

from keyboard import *
from db import *
from utils.utils_checkers import *

from ticTacToe import callback_handler_ticTacToe
from checkers import checkers_callback_handler

bot = Bot(token="823238605:AAHZGYqQKhyC9ywH29T346J3oqTFza6mKDY")
dp = Dispatcher(bot, storage=MemoryStorage())


class IsCallbackQuery(Filter):
	def __init__(self, word_):
		self.word = word_

	async def check(self, call: types.Message):
		return self.word in call.data

# Регистрация callback хендлеров
dp.register_callback_query_handler(callback_handler_ticTacToe, IsCallbackQuery(word_="plane_"))
dp.register_callback_query_handler(checkers_callback_handler, IsCallbackQuery(word_="place_"))

@dp.message_handler(commands="start")
async def send_welcome(message: types.Message):
	if "sender" in message.text: return await message.answer("К сожалению, в игры не встроена игра с ботом\nПоэтому отправляйся в чат с другом и играйте")
	await message.answer("Приветствую, я бот с играми. При помощи меня можно поиграть в игры на двоих в чате\n\n__Какие игры сейчас есть?__\n— На данный момент в бота встроено пока что две игры: Шашки и Крестики-нолики.\nЕсли у вас есть идеи, пишите разработчику\n\n__Как начать играть?__\n— Чтобы начать игру, перейдите в чат с другом и вызовите меня `@multi_games_bot`, после чего у вас появится меню с выбором игры. Нажмите на желаемую игру.", parse_mode=types.ParseMode.MARKDOWN)	

@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
	print(inline_query)
	if inline_query.chat_type == "sender":
		return await inline_query.answer([], is_personal=True, cache_time=60, switch_pm_parameter="sender", switch_pm_text="Нельзя играть с этим ботом")		
	item = [
		InlineQueryResultArticle(id=inline_query.id,title=f'Шашки',input_message_content=InputTextMessageContent("Шашки\nЧёрных ⚫️ - 12 | Белых ⚪️ - 12\nПервый ходит соперник! (белыми)"),reply_markup=checkers_markup(0),thumb_url="https://cdn6.aptoide.com/imgs/7/b/2/7b26460946c98ac243f2ff6cdbcdb53c_icon.png"),
		InlineQueryResultArticle(id=int(inline_query.id)+1,title=f'Крестики нолики',input_message_content=InputTextMessageContent("Крестики нолики\nПервый ходит соперник!"),reply_markup=start_markup(),thumb_url="https://banner2.cleanpng.com/20180613/cj/kisspng-square-meter-square-meter-5b21c13baa1dc7.9859413415289388116968.jpg")

	]
	await inline_query.answer(item, is_personal=True, cache_time=1)

@dp.chosen_inline_handler()
async def chosen_handler(chosen: ChosenInlineResult):
	place = await create_place()
	new_game_room(owner=chosen["from"].id, inline_id=chosen.inline_message_id, place=place, type_game="checkers")

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)