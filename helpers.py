import sqlite3
from blessed import Terminal


def queryDb(db_path):
	"""
	Get all games from an existing db file
	"""
	term = Terminal()

	# Empty list to contain game info
	game_details = []

	# Connect and create cursor
	connection = sqlite3.connect(db_path)
	cursor = connection.cursor()
	
	# Curse through each row in Games table
	for row in cursor.execute('SELECT * FROM Games;'):
		row_list = list(row)
		game_details.append(row_list)
	
	count = len(game_details)
	print(f"{term.purple}Retrieved {count} games from {db_path}{term.normal}")

	# Close connection
	connection.close()

	# Return game_details list
	return game_details