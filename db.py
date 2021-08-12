import json, os, psycopg2

def ensure_connection(func):
	def inner(*args, **kwargs):
		with psycopg2.connect(os.environ["DATABASE_URL"]) as conn:
			kwargs['conn'] = conn
			res = func(*args, **kwargs)
		return res
	return inner

# База юзеров
@ensure_connection
def new_user(conn, user_id: int):
	c = conn.cursor()
	c.execute('INSERT INTO users (user_id) VALUES (%s)', (user_id,))
	conn.commit()

@ensure_connection
def update_user(conn, user_id: int, index: str, value: str):
	c = conn.cursor()
	c.execute('UPDATE users SET {0} = %s WHERE user_id = %s'.format(index), (value, user_id))
	conn.commit()

@ensure_connection
def delete_user(conn, user_id: int):
	c = conn.cursor()
	c.execute('DELETE FROM users WHERE user_id=%s', (user_id,))
	conn.commit()

@ensure_connection
def get_user(conn, user_id: int):
	c = conn.cursor()
	c.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
	return c.fetchall()

@ensure_connection
def get_admins(conn, status: str):
	c = conn.cursor()
	c.execute('SELECT * FROM users WHERE status = %s', (status,))
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
	c.execute('INSERT INTO game_room (owner, inline_id) VALUES (%s,%s)', (owner, inline_id))
	conn.commit()

@ensure_connection
def get_game_room(conn, inline_id: str):
	c = conn.cursor()
	c.execute('SELECT * FROM game_room WHERE inline_id = %s', (inline_id,))
	return c.fetchall()

@ensure_connection
def update_game_room(conn, inline_id: str, index: str, value: str):
	c = conn.cursor()
	c.execute('UPDATE game_room SET {0} = %s WHERE inline_id = %s'.format(index), (value, inline_id))
	conn.commit()

@ensure_connection
def delete_game_room(conn, inline_id: int):
	c = conn.cursor()
	c.execute('DELETE FROM game_room WHERE inline_id=%s', (inline_id,))
	conn.commit()

if __name__ == '__main__':
	pass
