from aiogram import types
import json
import db

async def create_place():
	c = 0
	arr = []
	for x in range(8):
		arr.append([])
		for y in range(8):
			c+= 1
			if (c <= 28) and (not(28 <= c <= 44) and (c%2 == 0)):
				arr[x].append({f"place_{x}_{y}":"⚫️"})
			elif (c >= 45) and (c%2 == 0):
				arr[x].append({f"place_{x}_{y}":"⚪️"})
			else:
				arr[x].append({f"place_{x}_{y}":" "})				
		c+= 1		
	return arr

def create_markup(markup):
	c = 0
	for x in range(8):
		arr = []
		for y in range(8):
			c+= 1
			if (c <= 28) and (not(28 <= c <= 44) and (c%2 == 0)):
				arr.append(types.InlineKeyboardButton("⚫️", callback_data=f'place_{x}_{y}'))
			elif (c >= 45) and (c%2 == 0):
				arr.append(types.InlineKeyboardButton("⚪️", callback_data=f'place_{x}_{y}'))
			else:
				arr.append(types.InlineKeyboardButton(" ", callback_data=f'place_{x}_{y}'))
		c+= 1		
		markup.row(*arr)

async def get_array_place(array, index):
	for row_ in array:
		for dict_ in row_:
			for index_dict in dict_:
				if index_dict == index:
					return dict_[index_dict]

async def count_checkers(array):
	black = 0; white = 0
	for row_ in array:
		for dict_ in row_:
			for index_dict in dict_:
				if dict_[index_dict] in ["⚫️","⬛️"]:
					black += 1
				elif dict_[index_dict] in ["⚪️","⬜️"]:
					white += 1
	return (black, white)


def get_arr(array, markup, type_ = 0):
	for row_ in array:
		arr_ = []
		for dict_ in row_:
			for index_dict in dict_:
				arr_.append(types.InlineKeyboardButton(dict_[index_dict], callback_data=index_dict))
		markup.row(*arr_)
	if type_ == 1: 
		markup.add(types.InlineKeyboardButton("Начать заново", callback_data='restart_zero_game'))
		markup.add(types.InlineKeyboardButton("Выйти", callback_data='delete_zero_game'))

async def update_arr(array, index, value):
	for row_ in array:
		for dict_ in row_:
			for index_dict in dict_:
				if index_dict == index:
					dict_[index_dict] = value
					return array

async def replace_array(array, replace, value):
	for i,a in enumerate(array):
		if replace == a: 
			array[i] = value
			return array 

async def check_go_to(array, index, side, min_ = 0, max_ = 7):
	name_x_y = index.split("_")
	x = int(name_x_y[1]); y = int(name_x_y[2])
	y_1 = y - 1; y_2 = y + 1
	if side == "⚫️":
		x_1 = x + 1
	elif side == "⚪️":
		x_1 = x - 1		
	elif side in ["⬛️","⬜️"]:
		x_1 = x + 1; x_2 = x - 1
		if x_2 < min_:
			x_2 = x + 1
		elif x_2 > max_:
			x_2 = x - 1
				

		array_place = [f"place_{x_1}_{y_1}",f"place_{x_1}_{y_2}", f"place_{x_2}_{y_1}",f"place_{x_2}_{y_2}"]
		for place in array_place:
			answ = await get_array_place(array=array, index=place)
			if ((side == "⬛️") and (answ in ["⚪️","⬜️"])) or ((side == "⬜️") and (answ in ["⬛️","⚫️"])):
				if place == array_place[0]:
					place_check = f'place_{int(place.split("_")[1])+1}_{int(place.split("_")[2])-1}'
				elif place == array_place[1]:
					place_check = f'place_{int(place.split("_")[1])+1}_{int(place.split("_")[2])+1}'
				elif place == array_place[2]:
					place_check = f'place_{int(place.split("_")[1])-1}_{int(place.split("_")[2])-1}'
				else:
					place_check = f'place_{int(place.split("_")[1])-1}_{int(place.split("_")[2])+1}'
				array_place = await replace_array(array_place,place, place_check)

		return array_place

	if x_1 < min_: x_1 = x + 1
	elif x_1 > max_: x_1 = x - 1

	array_place = [f"place_{x_1}_{y_1}",f"place_{x_1}_{y_2}"]
	for place in array_place:
		answ = await get_array_place(array=array, index=place)
		if (side == "⚪️") and (answ in ["⬛️","⚫️"]):
			if place == array_place[0]:
				place_check = f'place_{int(place.split("_")[1])-1}_{int(place.split("_")[2])-1}'
			else:
				place_check = f'place_{int(place.split("_")[1])-1}_{int(place.split("_")[2])+1}'

			array_place = await replace_array(array_place,place, place_check)
		elif (side == "⚫️") and (answ in ["⚪️","⬜️"]):
			if place == array_place[0]:
				place_check = f'place_{int(place.split("_")[1])+1}_{int(place.split("_")[2])-1}'
			else:
				place_check = f'place_{int(place.split("_")[1])+1}_{int(place.split("_")[2])+1}'

			array_place = await replace_array(array_place,place, place_check)

	return array_place

async def checked_game_checkers(room, array, calldata, call, type_ = None):
	pos_ = await get_array_place(array=array, index=calldata)
	if type_ is None:
		if pos_ == " ":
			return "В этой области нет шашки"
		elif (call["from"].id == room[0]) and (pos_ == "⚪️") :
			return "Вы ходите чёрными, а не белыми"
		elif (call["from"].id == room[2]) and (pos_ == "⚫️"):
			return "Вы ходите белыми, а не чёрными"
		else: return False
	else:
		my_side = await get_array_place(array=array, index=json.loads(room[4])[1])
		if ((call["from"].id == room[0]) and (pos_ in ["⚫️","⬛️"])) or ((call["from"].id == room[2]) and (pos_ in ["⚪️","⬜️"])):
			db.update_game_room(inline_id=call.inline_message_id, index="going", value=json.dumps([call["from"].id, calldata]))
			return "Была выбрана другая шашка"
		elif ((call["from"].id == room[0]) and (pos_ in ["⚪️","⬜️"])) or ((call["from"].id == room[2]) and (pos_ in ["⚫️","⬛️"])):
			return "Нельзя ставить шашку на шашку"
		elif calldata not in await check_go_to(array=array, index=json.loads(room[4])[1], side=my_side):
			return "Эта шашка может ходить только по диагонали"
		# elif
		# if ((call["from"].id == room[0]) and (pos_ == "⚫️")) or ((call["from"].id == room[2]) and (pos_ == "⚪️")) :
			# return "Вы не можете поставить на свою же шашку"
		# elif (call["from"].id == room[2]) and (pos_ == "⚪️"):
			# return "Вы ходите белыми, а не чёрными"
		else: return False

async def checked_kill_checkers(my_pos, calldata):
	place_split = my_pos.split("_")
	x = int(place_split[1]); y = int(place_split[2]) 
	array_place = [f"place_{x+1}_{y+1}",f"place_{x-1}_{y+1}",f"place_{x+1}_{y-1}",f"place_{x-1}_{y-1}"]
	for place in array_place:
		place_split = place.split("_")
		x = int(place_split[1]); y = int(place_split[2]) 
		array = [f"place_{x+1}_{y+1}",f"place_{x-1}_{y+1}",f"place_{x+1}_{y-1}",f"place_{x-1}_{y-1}"]
		if calldata in array:
			return place



# if __name__ == '__main__':
	
# 	arr = [
# 		[{'place_0_0': ' '}, {'place_0_1': '⚫️'}, {'place_0_2': ' '}, {'place_0_3': '⚫️'}, {'place_0_4': ' '}, {'place_0_5': '⚫️'}, {'place_0_6': ' '}, {'place_0_7': '⚫️'}],
# 		[{'place_1_0': ' '}, {'place_1_1': ' '}, {'place_1_2': '⚫️'}, {'place_1_3': ' '}, {'place_1_4': '⚫️'}, {'place_1_5': ' '}, {'place_1_6': '⚫️'}, {'place_1_7': ' '}],
# 		[{'place_2_0': '⚫️'}, {'place_2_1': '⚫️'}, {'place_2_2': ' '}, {'place_2_3': '⚫️'}, {'place_2_4': ' '}, {'place_2_5': '⚫️'}, {'place_2_6': ' '}, {'place_2_7': '⚫️'}],
# 		[{'place_3_0': ' '}, {'place_3_1': ' '}, {'place_3_2': ' '}, {'place_3_3': ' '}, {'place_3_4': ' '}, {'place_3_5': ' '}, {'place_3_6': ' '}, {'place_3_7': ' '}],
# 		[{'place_4_0': ' '}, {'place_4_1': ' '}, {'place_4_2': ' '}, {'place_4_3': ' '}, {'place_4_4': ' '}, {'place_4_5': ' '}, {'place_4_6': ' '}, {'place_4_7': ' '}],
# 		[{'place_5_0': '⚪️'}, {'place_5_1': ' '}, {'place_5_2': '⚪️'}, {'place_5_3': ' '}, {'place_5_4': '⚪️'}, {'place_5_5': ' '}, {'place_5_6': '⚪️'}, {'place_5_7': ' '}],
# 		[{'place_6_0': ' '}, {'place_6_1': '⚪️'}, {'place_6_2': ' '}, {'place_6_3': '⚪️'}, {'place_6_4': ' '}, {'place_6_5': '⚪️'}, {'place_6_6': ' '}, {'place_6_7': '⚪️'}],
# 		[{'place_7_0': '⚪️'}, {'place_7_1': ' '}, {'place_7_2': '⚪️'}, {'place_7_3': ' '}, {'place_7_4': '⚪️'}, {'place_7_5': ' '}, {'place_7_6': '⚪️'}, {'place_7_7': ' '}]
# 	]
