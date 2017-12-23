import requests
import numpy as np
import pickle
import time

def scrape_nba():

	data = {}

	start_year = '00'
	end_year = '17'
	games_actual_season = 479

	base = '00000'

	games_in_list = pickle.load(open('C:/NBA/game_list.pkl', 'rb'))
	if games_in_list == []:
		games_list = []
	else:
		games_list = list(np.array(games_in_list)[:,0])

	for year in range(int(end_year) + 1):
		
		if year in [0,1,2,3]:
			games_per_season = 1189
		elif year == 11:
			games_per_season = 990
		elif year == 12:
			games_per_season = 1213
		else:	
			games_per_season = 1230
		
		if year < int(start_year):
			continue
		
		if year == end_year:
			number_of_games = games_actual_season
		else:
			number_of_games = games_per_season

		for game in range(number_of_games):

			if len(str(year)) == 1:
				year_ID = '0' + str(year)
			else:
				year_ID = str(year)

			line = game + 2
			dig = len(base) - len(str(game + 1))
			strip = base[:dig]
			count_ID = strip + str(game + 1)
			game_ID = '002' + year_ID + str(count_ID)

			if game_ID in games_list or game_ID[2:] in games_list:
				continue

			if game_ID == '21600266':
				continue

			if int(game_ID[-4:]) > number_of_games:
				break 				

			try:
				url_game = 'http://stats.nba.com/stats/boxscoresummaryv2?GameID=' + game_ID
				url_traditional = 'http://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange=28800&GameID=' + game_ID + '&RangeType=0&Season=2015-16&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
				url_advanced = 'http://stats.nba.com/stats/boxscoreadvancedv2?EndPeriod=10&EndRange=28800&GameID=' + game_ID + '&RangeType=0&Season=2015-16&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
				url_misc = 'http://stats.nba.com/stats/boxscoremiscv2?EndPeriod=10&EndRange=28800&GameID=' + game_ID + '&RangeType=0&Season=2015-16&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
				url_scoring = 'http://stats.nba.com/stats/boxscorescoringv2?EndPeriod=10&EndRange=28800&GameID=' + game_ID + '&RangeType=0&Season=2015-16&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
					
				u_a = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"

				response = requests.get(url_game, headers={"USER-AGENT":u_a})
				game_date = response.json()['resultSets'][0]['rowSet'][0][0]
				home_team_ID = response.json()['resultSets'][0]['rowSet'][0][6]
				visitor_team_ID = response.json()['resultSets'][0]['rowSet'][0][7]			
				
				response = requests.get(url_traditional, headers={"USER-AGENT":u_a})
				team_a_traditional = response.json()['resultSets'][1]['rowSet'][0]
				team_b_traditional = response.json()['resultSets'][1]['rowSet'][1]

				response = requests.get(url_advanced, headers={"USER-AGENT":u_a})
				team_a_advanced = response.json()['resultSets'][1]['rowSet'][0]
				team_b_advanced = response.json()['resultSets'][1]['rowSet'][1]

				response = requests.get(url_misc, headers={"USER-AGENT":u_a})
				team_a_misc = response.json()['resultSets'][1]['rowSet'][0]
				team_b_misc = response.json()['resultSets'][1]['rowSet'][1]

				response = requests.get(url_scoring, headers={"USER-AGENT":u_a})
				team_a_scoring = response.json()['resultSets'][1]['rowSet'][0]
				team_b_scoring = response.json()['resultSets'][1]['rowSet'][1]		

				response = requests.get(url_traditional, headers={"USER-AGENT":u_a})
			except:
				try:
					time.sleep(60)

					url_game = 'http://stats.nba.com/stats/boxscoresummaryv2?GameID=' + game_ID
					url_traditional = 'http://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange=28800&GameID=' + game_ID + '&RangeType=0&Season=2015-16&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
					url_advanced = 'http://stats.nba.com/stats/boxscoreadvancedv2?EndPeriod=10&EndRange=28800&GameID=' + game_ID + '&RangeType=0&Season=2015-16&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
					url_misc = 'http://stats.nba.com/stats/boxscoremiscv2?EndPeriod=10&EndRange=28800&GameID=' + game_ID + '&RangeType=0&Season=2015-16&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
					url_scoring = 'http://stats.nba.com/stats/boxscorescoringv2?EndPeriod=10&EndRange=28800&GameID=' + game_ID + '&RangeType=0&Season=2015-16&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
						
					u_a = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"

					response = requests.get(url_game, headers={"USER-AGENT":u_a})
					game_date = response.json()['resultSets'][0]['rowSet'][0][0]
					home_team_ID = response.json()['resultSets'][0]['rowSet'][0][6]
					visitor_team_ID = response.json()['resultSets'][0]['rowSet'][0][7]			
					
					response = requests.get(url_traditional, headers={"USER-AGENT":u_a})
					team_a_traditional = response.json()['resultSets'][1]['rowSet'][0]
					team_b_traditional = response.json()['resultSets'][1]['rowSet'][1]

					response = requests.get(url_advanced, headers={"USER-AGENT":u_a})
					team_a_advanced = response.json()['resultSets'][1]['rowSet'][0]
					team_b_advanced = response.json()['resultSets'][1]['rowSet'][1]

					response = requests.get(url_misc, headers={"USER-AGENT":u_a})
					team_a_misc = response.json()['resultSets'][1]['rowSet'][0]
					team_b_misc = response.json()['resultSets'][1]['rowSet'][1]

					response = requests.get(url_scoring, headers={"USER-AGENT":u_a})
					team_a_scoring = response.json()['resultSets'][1]['rowSet'][0]
					team_b_scoring = response.json()['resultSets'][1]['rowSet'][1]		

					response = requests.get(url_traditional, headers={"USER-AGENT":u_a})
				except:
					continue


			team_a_data = team_a_traditional + team_a_advanced + team_a_misc + team_a_scoring
			team_b_data = team_b_traditional + team_b_advanced + team_b_misc + team_b_scoring
			
			team_a_ID = team_a_traditional[1]
			team_b_ID = team_b_traditional[1]
			
			if team_a_traditional[23] > team_b_traditional[23]:
				team_a_win = 1
				team_b_win = 0
			else:
				team_a_win = 0
				team_b_win = 1

			game_list = [str(game_ID), game_date]

			if team_a_ID == home_team_ID and team_b_ID == visitor_team_ID:

				if team_a_win == 1:
					home_team_data = [1] + [1] + game_list + team_a_data
					visitor_team_data = [0] + [0] + game_list + team_b_data
					win_var = 1
					home_score = team_a_traditional[23]
					visitor_score = team_b_traditional[23]

				else:
					home_team_data = [1] + [0] + game_list + team_a_data
					visitor_team_data = [0] + [1] + game_list + team_b_data
					win_var = 0
					home_score = team_a_traditional[23]
					visitor_score = team_b_traditional[23]

			elif team_b_ID == home_team_ID and team_a_ID == visitor_team_ID:
				
				if team_a_win == 1:
					visitor_team_data = [0] + [1] + game_list + team_a_data
					home_team_data = [1] + [0] + game_list + team_b_data
					win_var = 0
					home_score = team_b_traditional[23]
					visitor_score = team_a_traditional[23]

				else:
					visitor_team_data = [0] + [0] + game_list + team_a_data
					home_team_data = [1] + [1] + game_list + team_b_data
					win_var = 1
					home_score = team_b_traditional[23]
					visitor_score = team_a_traditional[23]

			games_in_list.append(game_list + [home_team_ID, visitor_team_ID, home_score, visitor_score, win_var])
			print (game_list + [home_team_ID, visitor_team_ID, home_score, visitor_score, win_var])				

			teams = [home_team_ID, visitor_team_ID]

			season_ID = game_ID[2:5]

			if season_ID not in data:
				data[season_ID] = {}

			for team in teams:

				if team not in data[season_ID]:
					data[season_ID][team] = {}
			
				for player in response.json()['resultSets'][0]['rowSet']:

					if player[1] == team:
		
						player_ID = str(player[4])
						player_NAME = str(player[5])
						player_DATA = [game_ID]

						if player_ID not in data[season_ID][team]:
							data[season_ID][team][player_ID] = {}

						if game_ID not in data[season_ID][team][player_ID]:
							data[season_ID][team][player_ID][game_ID] = player

				if 'team_stats' not in data[season_ID][team]:
					data[season_ID][team]['team_stats'] = {}

				if game_ID not in data[season_ID][team]['team_stats']:

					if team == home_team_ID:
						data[season_ID][team]['team_stats'][game_ID] = home_team_data
					elif team == visitor_team_ID:
						data[season_ID][team]['team_stats'][game_ID] = visitor_team_data

				#print (season_ID, game_ID, team)
				
		with open('C:/NBA/data_all.pkl', 'wb') as f:
			pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

		with open('C:/NBA/game_list.pkl', 'wb') as f:
			pickle.dump(games_in_list, f, pickle.HIGHEST_PROTOCOL)

scrape_nba()
