from aiogram import Bot, Dispatcher, executor, types
import asyncio, os, json

from keyboard import *
from db import *
from utils.utils_checkers import *



# @dp.callback_query_handler()
async def checkers_callback_handler(call: types.CallbackQuery):
	inline_id = call.inline_message_id
	if "place_" in call.data:
		room = get_game_room(inline_id=inline_id)[0]

		if (room[2] is None) and (call["from"].id != room[0]):
			update_game_room(inline_id=inline_id, index="player_2", value=call["from"].id)

		try: going = json.loads(room[4])
		except Exception as e: pass
		try:
			if going == "end":
				return await call.answer(text="Игра завершина", show_alert=True)
		except Exception as e: pass

		if room[4] is None or (json.loads(room[4])[1] == "end" and json.loads(room[4])[0] != call["from"].id):
			asnwer_checked = await checked_game_checkers(room=room, array=json.loads(room[1]), calldata=call.data, call=call)
			if asnwer_checked:
				return await call.answer(asnwer_checked)

			update_game_room(inline_id=inline_id, index="going", value=json.dumps([call["from"].id, call.data]))
			return await call.answer("Нажмите на кнопку, куда хотите переместить шашку")
		elif going[0] != call["from"].id or (going[1] == "end" and going[0] == call["from"].id):
			return await call.answer("Сейчас ход соперника!")

		array = json.loads(room[1])
		checked_kill = await checked_kill_checkers(my_pos=going[1], calldata=call.data)
		if checked_kill is not None:
			array = await update_arr(array=array, index=checked_kill, value=" ")

		if call["from"].id == room[0]:
			asnwer_checked = await checked_game_checkers(room=room, array=json.loads(room[1]), calldata=call.data, call=call, type_="game")
			if asnwer_checked:
				return await call.answer(asnwer_checked)

			if call.data in ["place_7_0","place_7_1","place_7_2","place_7_3","place_7_4","place_7_5","place_7_6","place_7_7"]:
				array = await update_arr(array=array, index=call.data, value="⬛️")
			else:
				array = await update_arr(array=array, index=call.data, value=await get_array_place(array, index=going[1]))
		elif call["from"].id == room[2]:
			asnwer_checked = await checked_game_checkers(room=room, array=json.loads(room[1]), calldata=call.data, call=call, type_="game")
			if asnwer_checked:
				return await call.answer(asnwer_checked)

			if call.data in ["place_0_0","place_0_1","place_0_2","place_0_3","place_0_4","place_0_5","place_0_6","place_0_7"]:
				array = await update_arr(array=array, index=call.data, value="⬜️")
			else:
				array = await update_arr(array=array, index=call.data, value=await get_array_place(array, index=going[1]))

		array = await update_arr(array=array, index=going[1], value=" ")
		update_game_room(inline_id=inline_id, index="place", value=json.dumps(array))
		update_game_room(inline_id=inline_id, index="going", value=json.dumps([going[0], "end"]))

		black, white = await count_checkers(array)
		if (black == 0) or (white == 0):
			update_game_room(inline_id=inline_id, index="going", value=json.dumps("end"))
			return await bot.edit_message_text(inline_message_id=call.inline_message_id, text=f"Шашки\n{'Победа чёрных ⚫️'if white == 0 else 'Победа белых ⚪️'}", reply_markup=checkers_markup(2, array))
		await bot.edit_message_text(inline_message_id=call.inline_message_id, text=f"Шашки\nЧёрных ⚫️ - {black} | Белых ⚪️ - {white}", reply_markup=checkers_markup(1, array))
	
	if call.data == "restart_checkers":
		room = get_game_room(inline_id=call.inline_message_id)[0]
		update_game_room(inline_id=call.inline_message_id, index="going", value=room[2])
		update_game_room(inline_id=call.inline_message_id, index="place", value=json.dumps(await create_place()))
		return await bot.edit_message_text(inline_message_id=call.inline_message_id, text=f"Шашки\nПервый ходит <a href='tg://user?id={room[2]}'>соперник</a>! (белыми)", parse_mode="HTML", reply_markup=checkers_markup(0))
	elif call.data == "delete_checkers":
		room = get_game_room(inline_id=call.inline_message_id)[0]
		await bot.edit_message_text(inline_message_id=call.inline_message_id, text=f"Круто поиграли ☺️")
		delete_game_room(inline_id=call.inline_message_id)
		return await call.answer(text="Игра была удалена из чата")

	await call.answer()


# if __name__ == '__main__':
# 	executor.start_polling(dp, skip_updates=True)