"""
Fetch game data from IGDB
"""


import argparse
import pandas as pd
import sqlite3
from blessed import Terminal
from igdb_service import IGDB_Service
from helpers import queryDb


def main(client_id, client_secret, min_id, max_id, db_path, results):

	term = Terminal()
	result = term.royalblue # results will be printed in blue

	print(term.normal)

	# Headers
	table_headers = ["id", "title", "description", "genres", "release_data", "cover_image_id"]

	# List to contain game info and create DataFrame.
	# Gets info from existing database if it was passed in.
	if db_path is not None:
		game_details = queryDb(db_path)
		result_df = pd.DataFrame(game_details, columns=table_headers)
	else:
		result_df = pd.DataFrame(columns=table_headers)

	print(result_df)

	# Sort by id
	result_df.sort_values(by=['id'], inplace=True, ascending=True)

	# Instantiate service class
	service = IGDB_Service(client_id, client_secret)

	# Get games from CSV
	file_path = './Games-To-Add.csv'
	csv_df = pd.read_csv(file_path)
	games = csv_df.to_dict(orient='records')
	for game_dict in games:
		game_info = service.fetch_game_details(game_dict['Title'], game_dict['Id'])
		# Add game if its id doesn't exist in the DataFrame already, else update it.
		if game_info[0] not in result_df.values:
			result_df.iloc[len(result_df.index)] = game_info
		else:
			result_df.iloc[result_df['id'].searchsorted(game_info[0])] = game_info

	# Get games by id
	if min_id is not None and max_id is not None:
		for id in range(min_id, max_id):
			print(f"{term.slategray}[{id}]", end=" ")
			game_info = service.fetch_game_details("", id)
			# Add game if its id doesn't exist in the DataFrame already, else update it.
			if game_info[0] not in result_df.values:
				result_df.iloc[len(result_df.index)] = game_info
			else:
				result_df.iloc[result_df['id'].searchsorted(game_info[0])] = game_info

	# Sort by id
	result_df.sort_values(by=['id'], inplace=True, ascending=True)

	# Save result to csv, json, and/or db file
	if results is None:
		results = ["db"]
	for result in results:
		result = result.lower()
		match result:
			case "csv":
				csv_file = 'results.csv'
				result_df.to_csv(csv_file, index=False)
				print(f"{result}Results saved to {csv_file}{term.normal}")
			case "json":
				json_file = 'results.json'
				result_df.to_json(json_file, orient='records', indent=4)
				print(f"{result}Results saved to {json_file}{term.normal}")
			case "db":
				db_file = 'results.db'
				connection = sqlite3.connect(db_file)
				result_df.to_sql(name='Games', con=connection, if_exists='replace', index=False)
				print(f"{result}Results saved to {db_file}{term.normal}")

	# CSV
	# #"""
	# csv_file = 'results.csv'
	# result_df.to_csv(csv_file, index=False)
	# print(f"{result}Results saved to {csv_file}{term.normal}")
	# #"""

	# # JSON
	# #"""
	# json_file = 'results.json'
	# result_df.to_json(json_file, orient='records', indent=4)
	# print(f"{result}Results saved to {json_file}{term.normal}")
	# #"""
	
	# # SQLite
	# #"""
	# db_file = 'results.db'
	# connection = sqlite3.connect(db_file)
	# result_df.to_sql(name='Games', con=connection, if_exists='replace', index=False)
	# print(f"{result}Results saved to {db_file}{term.normal}")
	# #"""


if __name__ == '__main__':
	# Parse arguments
	parser = argparse.ArgumentParser(
		description="Script that gets video game information using IGDB's API"
	)
	parser.add_argument("--client_id", required=True, type=str)
	parser.add_argument("--client_secret", required=True, type=str)
	parser.add_argument("--min_id", required=False, type=int)
	parser.add_argument("--max_id", required=False, type=int)
	parser.add_argument("--db_path", required=False, type=str)
	parser.add_argument("--results", required=False, type=list[str])
	args = parser.parse_args()

	client_id = args.client_id
	client_secret = args.client_secret
	db_path = args.db_path
	min_id = args.min_id
	max_id = args.max_id
	results = args.results

	# Run main()
	main(client_id, client_secret, min_id, max_id, db_path, results)
