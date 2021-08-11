from aiogram import types
from db import get_game_room, update_game_room
import json
from utils.utils_checkers import *

def start_game(type_button):
	markup = types.InlineKeyboardMarkup()
	markup.add(types.InlineKeyboardButton('Играть',callback_data=type_button))
	return markup

def zero_game_markup():
	markup = types.InlineKeyboardMarkup()
	# arr = []
	# for x in range(3):
	# 	arr.append([])		
	# 	for y in range(3):
	# 		arr[x].append(f"{x}_{y}")

	# for 
	# row_btns = (types.InlineKeyboardButton("🔥", callback_data=data) for text in arr)

	# print(*arr)
	# arr = (types.InlineKeyboardButton(data, callback_data=f"place_{index}") for index,data in enumerate(["🔥" for _ in range(9)]))
	# markup.row(*arr)
	markup.add(types.InlineKeyboardButton('🔥', callback_data='plane_0'), types.InlineKeyboardButton('🔥', callback_data='plane_1'), types.InlineKeyboardButton('🔥', callback_data='plane_2'))
	markup.add(types.InlineKeyboardButton('🔥', callback_data='plane_3'), types.InlineKeyboardButton('🔥', callback_data='plane_4'), types.InlineKeyboardButton('🔥', callback_data='plane_5'))
	markup.add(types.InlineKeyboardButton('🔥', callback_data='plane_6'), types.InlineKeyboardButton('🔥', callback_data='plane_7'), types.InlineKeyboardButton('🔥', callback_data='plane_8'))
	return markup

def update_inline_markup(inline_message_id, place):
	markup = types.InlineKeyboardMarkup()
	update_game_room(inline_id=inline_message_id, index="place", value=json.dumps(place))
	room = json.loads(get_game_room(inline_id=inline_message_id)[0][1])
	markup.add(types.InlineKeyboardButton(room[0], callback_data='plane_0'), types.InlineKeyboardButton(room[1], callback_data='plane_1'), types.InlineKeyboardButton(room[2], callback_data='plane_2'))
	markup.add(types.InlineKeyboardButton(room[3], callback_data='plane_3'), types.InlineKeyboardButton(room[4], callback_data='plane_4'), types.InlineKeyboardButton(room[5], callback_data='plane_5'))
	markup.add(types.InlineKeyboardButton(room[6], callback_data='plane_6'), types.InlineKeyboardButton(room[7], callback_data='plane_7'), types.InlineKeyboardButton(room[8], callback_data='plane_8'))

	game_room_going = get_game_room(inline_id=inline_message_id)[0]
	if game_room_going[4] == "end":
		markup.add(types.InlineKeyboardButton("Начать заново", callback_data='restart_zero_game'))
		markup.add(types.InlineKeyboardButton("Выйти", callback_data='delete_zero_game'))
	return markup


def checkers_markup(index, array_markup = None):
	markup = types.InlineKeyboardMarkup()
	if index == 0:
		create_markup(markup)
	elif index == 1:
		get_arr(array_markup, markup)
	else:
		get_arr(array_markup, markup, type_=1)


	return markup