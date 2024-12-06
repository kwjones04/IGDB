"""
IGDB service class to interact with IGDB's API
"""

import requests
import math
from datetime import datetime
from blessed import Terminal

class IGDB_Service:
	"""
	IGDB service class to interact with IGDB's API
	"""

	def __init__(self, client_id, client_secret):
		self._client_id = client_id
		self._client_secret = client_secret

		self._normal = Terminal().normal
		self._success = Terminal().green
		self._failure = Terminal().red
		self._warning = Terminal().yellow

		self._access_token = self.__fetch_access_token()

	def __fetch_access_token(self):
		"""
		Fetch access token given a client id and client secret.
		"""
		# Request details
		request_url = f"https://id.twitch.tv/oauth2/token?client_id={self._client_id}&client_secret={self._client_secret}&grant_type=client_credentials"

		# POST request
		response = requests.post(request_url)

		# Success
		if response.status_code == 200:
			access_data = response.json()
			if 'access_token' in access_data:
				print(f'{self._success}IGDB request for access token succeeded{self._normal}')
				print(f"Access Token: {access_data['access_token']}")
				return access_data['access_token']
		# Failure
		else:
			print(f'{self._failure}IGDB request for access token failed with status code {response.status_code}.{self._normal}')
			return
	
	def __fetch_platform_name(self, platform_id):
		"""
		Fetch a platform's name given the platform id
		"""
		# Request details
		request_url = 'https://api.igdb.com/v4/platforms'
		request_headers = {
			'Client-ID': self._client_id,
			'Authorization': f'Bearer {self._access_token}'
		}
		request_body = f"fields name; where id={platform_id}; limit 1;"

		# POST request
		response = requests.post(request_url, headers=request_headers, data=request_body)

		# Success
		if response.status_code == 200:
			platform_data = response.json()
			if platform_data:
				return platform_data[0].get('name', 'N/A')
		# Failure
		else:
			print(f"{self._failure}IGDB platforms request failed with status code {response.status_code}{self._normal}")
			return "N/A"
		
	def __fetch_release_dates_and_platforms(self, game_id):
		"""
		Fetch platform and release date for platform, given a game's id
		"""
		# Request details
		request_url = 'https://api.igdb.com/v4/release_dates'
		request_headers = {
			'Client-ID': self._client_id,
			'Authorization': f'Bearer {self._access_token}'
		}
		request_body = f"fields date, platform; where game={game_id}; sort date desc;"

		# POST request
		response = requests.post(request_url, headers=request_headers, data=request_body)

		# Success
		if response.status_code == 200:
			data = response.json()
			release_data = {}
			for entry in data:
				if 'platform' in entry:
					platform = self.__fetch_platform_name(entry['platform'])
					if 'date' in entry:
						release_data[platform] = datetime.utcfromtimestamp(entry['date']).strftime('%Y-%m-%d')
					else:
						release_data[platform] = 'N/A'
				else:
					release_data['N/A'] = 'N/A'
			return release_data
		# Failure
		else:
			print(f"{self._failure}IGDB release dates request failed with status code {response.status_code}{self._normal}")
			return {'N/A': 'N/A'}
	
	def fetch_game_details(self, title, game_id):
		"""
		Fetch game details for a given title or id string.
		"""
		# Request details
		request_url = 'https://api.igdb.com/v4/games'
		request_headers = {
			'Client-ID': self._client_id,
			'Authorization': f'Bearer {self._access_token}'
		}

		# Id column is optional and only used in case title doesn't retrieve the expected output
		if math.isnan(game_id):
			request_body = f"fields id, name, summary, genres.name, themes.name, cover.image_id; where name=\"{title}\"; limit 1;"
		else:
			game_id = int(game_id)
			request_body = f"fields id, name, summary, genres.name, themes.name, cover.image_id; where id={game_id}; limit 1;"
		
		# POST request
		response = requests.post(request_url, headers=request_headers, data=request_body)

		# Success
		if response.status_code == 200:
			igdb_data = response.json()
			if igdb_data:
				game = igdb_data[0]
				game_id = game.get('id')
				game_title = game.get('name', 'N/A')
				game_description = game.get('summary', 'N/A')
				genres = ", ".join([g.get('name', 'N/A') for g in game.get('genres', [{'name': 'N/A'}])])
				cover_info =  game.get('cover', 'N/A')
				cover_image_id = 'N/A'
				if cover_info != 'N/A':
					try:
						cover_image_id = cover_info['image_id']
					except:
						pass

				# platform and release date for platform
				dict_data = []
				for platform, date in self.__fetch_release_dates_and_platforms(game_id).items():
					dict_data.append(f"{platform}: {date}")
				release_data = ", ".join(entry for entry in dict_data)

				# Place data in list to return
				game_data = [game_id, game_title, game_description, genres, release_data, cover_image_id]

				# Prints missing information if any
				if 'N/A' in game_data or 'N/A: N/A' in game_data:
					indices = []
					for i in range(len(game_data)):
						if game_data[i] == 'N/A' or game_data[i] == 'N/A: N/A':
							indices.append(i)
					print(f"{self._warning}Missing information for {game_title}: {indices}{self._normal}")
				else:
					print(f"{self._success}Retrieved information for {game_title}{self._normal}")

				# Return data
				return game_data
			else:
				print(f"{self._failure}No information for {title}{self._normal}")
				return ['N/A', title, 'N/A', 'N/A', 'N/A', 'N/A']
		# Failure
		else:
			print(f"{self._failure}IGDB request for {title} failed with status code {response.status_code}{self._normal}")
			print(response.reason)
			return ['N/A', title, 'N/A', 'N/A', 'N/A', 'N/A']
