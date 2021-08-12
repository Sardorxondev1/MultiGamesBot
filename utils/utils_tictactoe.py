import json


async def checked_click_button(place, button):  # Проверяет является ли место куда кликнули занятым
	button = button.split("plane_")[1]
	return place[int(button)] != "🔥"