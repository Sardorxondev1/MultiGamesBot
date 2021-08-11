import sqlite3, random, json

def ensure_connection(func):
	def inner(*args, **kwargs):
		with sqlite3.connect('database.db') as conn:
			kwargs['conn'] = conn
			res = func(*args, **kwargs)
		return res

	return inner

# База юзеров
@ensure_connection
def new_user(conn, user_id: int):
	c = conn.cursor()
	c.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
	conn.commit()

@ensure_connection
def update_user(conn, user_id: int, index: str, value: str):
	c = conn.cursor()
	c.execute('UPDATE users SET {0} = ? WHERE user_id = ?'.format(index), (value, user_id))
	conn.commit()

@ensure_connection
def delete_user(conn, user_id: int):
	c = conn.cursor()
	c.execute('DELETE FROM users WHERE user_id=?', (user_id,))
	conn.commit()

@ensure_connection
def get_user(conn, user_id: int):
	c = conn.cursor()
	c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
	return c.fetchall()

@ensure_connection
def get_admins(conn, status: str):
	c = conn.cursor()
	c.execute('SELECT * FROM users WHERE status = ?', (status,))
	return c.fetchall()

@ensure_connection
def get_all_users(conn):
	c = conn.cursor()
	c.execute('SELECT * FROM users')
	return c.fetchall()

# База игр

@ensure_connection
def new_game_room(conn, owner: int, inline_id: str):
	c = conn.cursor()
	# if type_game == "checkers":
	# 	place = json.dumps(place)
	# else:
	# 	place = json.dumps(["🔥" for _ in range(9)])
	c.execute('INSERT INTO game_room (owner, inline_id) VALUES (?,?)', (owner, inline_id))
	conn.commit()

# @ensure_connection
# def new_game_room(conn, owner: int, inline_id: str, type_game: str = "zero-game", place: str = None):
# 	c = conn.cursor()
# 	if type_game == "checkers":
# 		place = json.dumps(place)
# 	else:
# 		place = json.dumps(["🔥" for _ in range(9)])
# 	c.execute('INSERT INTO game_room (owner, place, inline_id, type_game) VALUES (?,?,?,?)', (owner, place, inline_id, type_game))
# 	conn.commit()

@ensure_connection
def get_game_room(conn, inline_id: str):
	c = conn.cursor()
	c.execute('SELECT * FROM game_room WHERE inline_id = ?', (inline_id,))
	return c.fetchall()

@ensure_connection
def update_game_room(conn, inline_id: str, index: str, value: str):
	c = conn.cursor()
	c.execute('UPDATE game_room SET {0} = ? WHERE inline_id = ?'.format(index), (value, inline_id))
	conn.commit()

@ensure_connection
def delete_game_room(conn, inline_id: int):
	c = conn.cursor()
	c.execute('DELETE FROM game_room WHERE inline_id=?', (inline_id,))
	conn.commit()

if __name__ == '__main__':
	pass

	# a = json.loads(get_game_room(inline_id="AgAAAM9aAQCicFo0lKPafLEIGjs")[0][1])
	# a = get_game_room(inline_id="AgAAAM9aAQCicFo0lKPafLEIGjs")[0][1]
	# print(a)