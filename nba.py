import requests
import csv
import numpy as np
import pandas as pd
import pickle
import time
from datetime import date
from math import exp
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier, ExtraTreesClassifier, GradientBoostingClassifier, RandomForestClassifier, VotingClassifier
from sklearn.naive_bayes import BernoulliNB, GaussianNB, MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from sklearn.feature_selection import RFECV
import xgboost
from xgboost.sklearn import XGBClassifier

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

def load_nba(state, form_list):

	if state == 'scrape':
		data = pickle.load(open('C:/NBA/data_all.pkl', 'rb'))
		game_list = pickle.load(open('C:/NBA/game_list.pkl', 'rb'))
	else:
		data = {}
		for form in form_list:
			data[form] = pickle.load(open('C:/NBA/season_avg_' + str(form) + '.pkl', 'rb'))
		data['org'] = pickle.load(open('C:/NBA/data_all.pkl', 'rb'))
		game_list = pickle.load(open('C:/NBA/game_list.pkl', 'rb'))

		for game in game_list:
			game[1] = int(game[1][:10].replace('-',''))
			#print (game)
	#quit()

	return data, game_list

def get_lists(data):

	team_list = []
	player_list = []

	for season in sorted(data):
		for team in data[season]:
			for stat_unit in data[season][team]:
				for game in sorted(data[season][team][stat_unit]):
					if stat_unit == 'team_stats':
						
						game_data = data[season][team][stat_unit][game][:2] + data[season][team][stat_unit][game][10:29] + data[season][team][stat_unit][game][35:50] + data[season][team][stat_unit][game][56:68] + data[season][team][stat_unit][game][74:]
						line_item = []
						for item in game_data:
							if type(item) == str or item == team:
								continue
							else:
								line_item.append(item)
						team_list.append(line_item)

					else:
						
						game_data = data[season][team][stat_unit][game][8:]
						line_item = []
						for item in game_data:
							if type(item) == str and ':' in item:
								item = item.replace(':','.')
								line_item.append(float(item))
							elif item == None:
								line_item.append(0.0)
							else:
								line_item.append(item)
						player_list.append(line_item)

	min_team_list = []
	max_team_list = []
	team_list_array = np.array(team_list)
	for i in range(team_list_array.shape[1]):
		min_team_list.append(min(list(team_list_array[:,i])))
		max_team_list.append(max(list(team_list_array[:,i])))

	min_player_list = []
	max_player_list = []
	player_list_array = np.array(player_list)
	for i in range(player_list_array.shape[1]):
		min_player_list.append(min(list(player_list_array[:,i])))
		max_player_list.append(max(list(player_list_array[:,i])))

	#print (min_team_list)
	#print (max_team_list)
	#print (min_player_list)
	#print (max_player_list)
	#quit()
	return min_team_list, max_team_list, min_player_list, max_player_list

def get_season_data(data, form, min_team_list, max_team_list, min_player_list, max_player_list):

	data_season = {}
	mf = 1
	for season in sorted(data):
		data_season[season] = {} 
		for team in data[season]:
			data_season[season][team] = {} 
			for stat_unit in data[season][team]:
				data_season[season][team][stat_unit] = {}
				data_season_array = []
				for game in sorted(data[season][team][stat_unit]):
					print (form,season,team,stat_unit,game)
					if stat_unit == 'team_stats':
						#sigmoid_scale = [4,7,10,24,27,28,29,31,32,33,35,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63]
						sigmoid_scale = []
						#################################################################################################	


						game_data = data[season][team][stat_unit][game][:2] + data[season][team][stat_unit][game][10:29] + data[season][team][stat_unit][game][35:50] + data[season][team][stat_unit][game][56:68] + data[season][team][stat_unit][game][74:]
						line_item = []
						for item in game_data:
							if type(item) == str or item == team:
								continue
							else:
								line_item.append(item)

						data_season_array.append(line_item)
						data_season_output = np.array(data_season_array) 

						season_averages = []
						for i in range(data_season_output.shape[1]):
							
							if form == 'all':
								if len(data_season_output[:,i]) == 0:
									var_mean = np.mean(data_season_output[:,i])
								else:
									var_mean = data_season_output[:,i][0]

								var_min = min_team_list[i]
								var_max = max_team_list[i]

								if var_min >= 0.0 and var_max <= 1.0:
									var = exp((var_mean*mf)-(mf/2)) / (exp((var_mean*mf)-(mf/2)) + 1)
								else:
									var = (var_mean - var_min) / (var_max - var_min)

								#print (var, var_mean, var_min, var_max)

							else:
								game_count = data_season_output.shape[0] - min(form, data_season_output.shape[0])
								if len(data_season_output[:,i]) == 0:
									var_mean = np.mean(data_season_output[game_count:,i])
								else:
									var_mean = data_season_output[game_count:,i][0]
								
								var_min = min_team_list[i]
								var_max = max_team_list[i]

								if var_min >= 0.0 and var_max <= 1.0:
									var = exp((var_mean*mf)-(mf/2)) / (exp((var_mean*mf)-(mf/2)) + 1)
								else:
									var = (var_mean - var_min) / (var_max - var_min)

								#print (var, var_mean, var_min, var_max)

							season_averages.append(var)

						home_games = 0
						away_games = 0
						home_win = 0
						away_win = 0
						if form == 'all':
							for game_data in data_season_output:

								# HOME GAMES
								if game_data[0] == 1:
									home_games += 1
								else:
									away_games += 1

								# HOME WIN
								if game_data[0] == 1 and game_data[1] == 1:
									home_win += 1
								
								# AWAY WIN
								if game_data[0] == 0 and game_data[1] == 1:
									away_win += 1
						else:
							game_count = data_season_output.shape[0] - min(form, data_season_output.shape[0])
							for game_data in data_season_output[game_count:]:

								# HOME GAMES
								if game_data[0] == 1:
									home_games += 1
								else:
									away_games += 1

								# HOME WIN
								if game_data[0] == 1 and game_data[1] == 1:
									home_win += 1
								
								# AWAY WIN
								if game_data[0] == 0 and game_data[1] == 1:
									away_win += 1								

						try:
							win_percentage = (home_win + away_win) / (home_games + away_games)
						except:
							win_percentage = 0.0

						try:
							home_win_percentage = float(home_win) / float(home_games)
						except:
							home_win_percentage = 0.0

						try:
							away_win_percentage = float(away_win) / float(away_games)
						except:
							away_win_percentage = 0.0

						try:
							fg = float(season_averages[2]) / float(season_averages[3])
							fg = exp((fg*mf)-(mf/2)) / (exp((fg*mf)-(mf/2)) + 1)
						except:
							fg = 0.0

						try:
							f3 = float(season_averages[5]) / float(season_averages[6])
							f3 = exp((f3*mf)-(mf/2)) / (exp((f3*mf)-(mf/2)) + 1)
						except:
							f3 = 0.0

						try:
							ft = float(season_averages[8]) / float(season_averages[9])
							ft = exp((ft*mf)-(mf/2)) / (exp((ft*mf)-(mf/2)) + 1)
						except:
							ft = 0.0

						season_averages = season_averages + [fg, f3, ft, win_percentage, home_win_percentage, away_win_percentage]
						#print (type(season_averages))
						data_season[season][team][stat_unit][game] = season_averages
					else:
						#sigmoid_scale = [3,6,9]
						sigmoid_scale = []
						#######################

						game_data = data[season][team][stat_unit][game][8:]
						line_item = []
						for item in game_data:
							if type(item) == str and ':' in item:
								item = item.replace(':','.')
								line_item.append(float(item))
							elif item == None:
								line_item.append(0.0)
							else:
								line_item.append(item)

						if line_item[0] != 0.0:
							data_season_array.append(line_item)
						
						data_season_output = np.array(data_season_array)

						if list(data_season_output) == [] and line_item[0] == 0.0:
							season_averages = []
							season_averages.append(list(np.zeros(23)))
							continue

						season_averages = []
						for i in range(data_season_output.shape[1]):

							if form == 'all':
								
								if len(data_season_output[:,i]) == 0:
									var_mean = data_season_output[:,i][0]
								else:
									var_mean = np.mean(data_season_output[:,i])
								
								var_min = min_player_list[i]
								var_max = max_player_list[i]

								if i in sigmoid_scale:
									var = exp((var_mean*mf)-(mf/2)) / (exp((var_mean*mf)-(mf/2)) + 1)
								else:
									var = (var_mean - var_min) / (var_max - var_min)

								#print (var, var_mean, var_min, var_max)

							else:
								game_count = data_season_output.shape[0] - min(form, data_season_output.shape[0])
								#print (game_count)
								#print (data_season_output.shape[0])
								#print (min(form, data_season_output.shape[0]))
								#quit()
								
								if len(data_season_output[:,i]) == 0:
									var_mean = data_season_output[game_count:,i][0]
								else:
									var_mean = np.mean(data_season_output[game_count:,i])

								var_mean = np.mean(data_season_output[game_count:,i])
								var_min = min_player_list[i]
								var_max = max_player_list[i]

								if i in sigmoid_scale:
									var = exp((var_mean*mf)-(mf/2)) / (exp((var_mean*mf)-(mf/2)) + 1)
								else:
									var = (var_mean - var_min) / (var_max - var_min)

								#print (var, var_mean, var_min, var_max)
							
							season_averages.append(var)
						try:
							fg = float(season_averages[1]) / float(season_averages[2])
							fg = exp((fg*mf)-(mf/2)) / (exp((fg*mf)-(mf/2)) + 1)
						except:
							fg = 0.0

						try:
							f3 = float(season_averages[4]) / float(season_averages[5])
							f3 = exp((f3*mf)-(mf/2)) / (exp((f3*mf)-(mf/2)) + 1)
						except:
							f3 = 0.0

						try:
							ft = float(season_averages[7]) / float(season_averages[8])
							ft = exp((ft*mf)-(mf/2)) / (exp((ft*mf)-(mf/2)) + 1)
						except:
							ft = 0.0

						data_season[season][team][stat_unit][game] = season_averages + [fg, f3, ft]

	with open('C:/NBA/season_avg_' + str(form) + '.pkl', 'wb') as f:
		pickle.dump(data_season, f, pickle.HIGHEST_PROTOCOL)

	return None

def days_since_game_generator(game_date, prev_date):
	
	game_year = int(game_date[:4])
	game_month = int(game_date[4:6])
	game_day = int(game_date[6:8])

	prev_year = int(prev_date[:4])
	prev_month = int(prev_date[4:6])
	prev_day = int(prev_date[6:8])	

	d0 = date(game_year, game_month, game_day)
	d1 = date(prev_year, prev_month, prev_day)
	delta = d0 - d1
	days_since_game = float(min(5,max(1,delta.days))) / 5.0
	
	return days_since_game

def get_date_array(team_array, num_vector):

	team_array = list(np.array(team_array)[len(team_array) - num_vector - 1:,1])

	date_array = []
	for i in range(len(team_array)):
		
		if i == 0:
			continue

		days = days_since_game_generator(team_array[i], team_array[i - 1])
		date_array.append(days)

	return date_array

def create_data(data, game_list):

	game_count = 0
	data_array = []

	for game in game_list:
		
		game_ID = game[0]
		season_ID = game[0][2:5]
		home_team_ID = game[2]
		away_team_ID = game[3]
		result = [game[6]]

		# SCHEDULE
		home_team_array = []
		away_team_array = []
		comp_count = 0

		for comp_game in game_list:

			if int(season_ID) < int(comp_game[0][2:5]):
				break

			if season_ID == comp_game[0][2:5] and comp_count <= game_count: 
				if home_team_ID == comp_game[2] or home_team_ID == comp_game[3]:
					home_team_array.append(comp_game)
				if away_team_ID == comp_game[2] or away_team_ID == comp_game[3]:
					away_team_array.append(comp_game)

			comp_count += 1

		if len(home_team_array) <= 10 or len(away_team_array) <= 10:
			game_count += 1
			continue

		home_date_array_1 = get_date_array(home_team_array, 1)
		home_date_array_3 = get_date_array(home_team_array, 3)
		home_date_array_5 = get_date_array(home_team_array, 5)
		home_date_array_10 = get_date_array(home_team_array, 10)

		away_date_array_1 = get_date_array(away_team_array, 1)
		away_date_array_3 = get_date_array(away_team_array, 3)
		away_date_array_5 = get_date_array(away_team_array, 5)
		away_date_array_10 = get_date_array(away_team_array, 10)

		home_date_array = home_date_array_1 + home_date_array_3 + home_date_array_5 + home_date_array_10
		away_date_array = away_date_array_1 + away_date_array_3 + away_date_array_5 + away_date_array_10
		full_date_array = home_date_array + away_date_array

		# SEASON
		if season_ID == '210':
			season_vec = [1,0,0,0,0,0,0,0]
		elif season_ID == '211':
			season_vec = [0,1,0,0,0,0,0,0]
		elif season_ID == '212':
			season_vec = [0,0,1,0,0,0,0,0]
		elif season_ID == '213':
			season_vec = [0,0,0,1,0,0,0,0]
		elif season_ID == '214':
			season_vec = [0,0,0,0,1,0,0,0]
		elif season_ID == '215':
			season_vec = [0,0,0,0,0,1,0,0]
		elif season_ID == '216':
			season_vec = [0,0,0,0,0,0,1,0]
		elif season_ID == '217':
			season_vec = [0,0,0,0,0,0,0,1]

		# GET PLAYER DATA HOME TEAM
		home_team_season = []
		game_ID_prev = home_team_array[-2][0]
		for player in data['all'][season_ID][home_team_ID]:
			played_games = len(data['all'][season_ID][home_team_ID][player])
			if player != 'team_stats' and game_ID in data['all'][season_ID][home_team_ID][player] and played_games > 5:				
				home_team_season.append([data['all'][season_ID][home_team_ID][player][game_ID][0],player])
		
		home_team_season = np.array(sorted(home_team_season, key=lambda x: x[0], reverse=True))
		home_team_season = list(home_team_season[:,1])
		home_team_data = []
		home_team_players = []
		player_count = 0
		for player in home_team_season:
			player_match = False
			for i in range(2,len(home_team_array)):
				home_team_match =  home_team_array[-i][0]
				if home_team_match in data['all'][season_ID][home_team_ID][player]:
					home_team_players.append(player)
					for var in data['all'][season_ID][home_team_ID][player][home_team_match]:
						home_team_data.append(var)
					player_match = True
					break

			if player_match == True:
				player_count += 1

				if player_count == 6:
					break

		# GET PLAYER DATA AWAY TEAM
		away_team_season = []
		game_ID_prev = away_team_array[-2][0]
		for player in data['all'][season_ID][away_team_ID]:
			played_games = len(data['all'][season_ID][away_team_ID][player])
			if player != 'team_stats' and game_ID in data['all'][season_ID][away_team_ID][player] and game_ID_prev in data['all'][season_ID][away_team_ID][player] and played_games > 5:	
				away_team_season.append([data['all'][season_ID][away_team_ID][player][game_ID][0],player])

		away_team_season = np.array(sorted(away_team_season, key=lambda x: x[0], reverse=True))
		away_team_season = list(away_team_season[:,1])
		away_team_data = []
		away_team_players = []
		player_count = 0
		for player in away_team_season:
			player_match = False
			for i in range(2,len(home_team_array)):
				away_team_match =  away_team_array[-i][0]
				if away_team_match in data['all'][season_ID][away_team_ID][player]:
					away_team_players.append(player)
					for var in data['all'][season_ID][away_team_ID][player][away_team_match]:
						away_team_data.append(var)
					player_match = True
					break

			if player_match == True:
				player_count += 1

				if player_count == 6:
					break

		# GET HOME TEAM DATA
		home_avg_3 = data[3][season_ID][home_team_ID]['team_stats'][home_team_match]
		home_avg_5 = data[5][season_ID][home_team_ID]['team_stats'][home_team_match]
		home_avg_10 = data[10][season_ID][home_team_ID]['team_stats'][home_team_match]
		home_avg_season = data['all'][season_ID][home_team_ID]['team_stats'][home_team_match]
		home_avg_data = home_avg_season + home_avg_10 + home_avg_5 + home_avg_3

		# GET AWAY TEAM DATA
		away_avg_3 = data[3][season_ID][away_team_ID]['team_stats'][away_team_match]
		away_avg_5 = data[5][season_ID][away_team_ID]['team_stats'][away_team_match]
		away_avg_10 = data[10][season_ID][away_team_ID]['team_stats'][away_team_match]
		away_avg_season = data['all'][season_ID][away_team_ID]['team_stats'][away_team_match]
		away_avg_data = away_avg_season + away_avg_10 + away_avg_5 + away_avg_3

		data_item = result + full_date_array + season_vec + home_team_data + away_team_data + home_avg_data + away_avg_data
		#data_item = result + home_date_array_5 + away_date_array_5 + season_vec + home_avg_10 + away_avg_10
		
		data_array.append(data_item)
		
		print (game_ID, home_team_ID, home_team_match, away_team_ID, away_team_match, len(data_item), len(result), len(full_date_array), len(season_vec), len(home_team_data), len(away_team_data), len(home_avg_data), len(away_avg_data))
		if len(data_item) != 875:
		#	print (len(data_item))
			quit()
		#if home_team_ID == 1610612761 and game_ID == '0021000263':
		#	print (home_team_season)
		#	quit()
		game_count += 1

	#data_array = np.array(data_array)

	return data_array

def create_game_list(game_list):

	for i in range(len(game_list)):

		if i == 0:
			continue
		if i == len(game_list)-1:
			break

		if game_list[i - 1][1] == game_list[i + 1][1]:
			game_list[i][1] = game_list[i - 1][1]

		if game_list[i][1] < game_list[i - 1][1] or game_list[i][1] > game_list[i + 1][1]:
			if game_list[i][1] - game_list[i - 1][1] > 15:
				if str(game_list[i + 1][1])[:6] == str(game_list[i - 1][1])[:6]:
					date_diff = max(1,int((game_list[i + 1][1] - game_list[i - 1][1]) / 2))
					game_list[i][1] = int(game_list[i - 1][1] + date_diff)
				else:
					game_list[i][1] = int(game_list[i - 1][1])	

	return game_list

def train_classifier_xgboost():

	seed = 24
	data = pickle.load(open('C:/NBA/data_games.pkl', 'rb'))
	
	## MANUAL SELECTION ##################################################
	#model = 4
	#
	#var_sheet = pd.read_csv('C:/NBA/NBA_sheet.csv', sep=';')
	#var_sheet = var_sheet.as_matrix()
	#var_list = []
	#for item in var_sheet:
	#	if item[model] == 'active':
	#		var_list.append(item[0])
	#
	#data_selected = []
	#for row in data:
	#	row_selected = []
	#	for i in range(len(row)):
	#		if i in var_list:
	#			row_selected.append(row[i])
	#	data_selected.append(row_selected)
	#data = data_selected
	######################################################################	

	## BASE SCORE ########################################################
	#home_win = 0
	#away_win = 0
	#total = 0
	#for item in labels:
	#	if item == 1:
	#		home_win += 1
	#	if item == 0:
	#		away_win += 1
	#	total += 1
	#print (home_win/total)
	#print (away_win/total)
	######################################################################

	data = np.array(data)

	features = data[:,1:].astype(float)
	labels = data[:,0]

	data_frame = pd.DataFrame(features)

	model_list = []
	model_selection = 'None'
	accuracy_model = 0.0
	first_var = True
	for i_model in range(features.shape[1]):
		accuracy_var = 0.0
		for i_var in range(features.shape[1]):
		
			if first_var == True:
				test_selection = data_frame[i_var]
				test_selection = test_selection.as_matrix().reshape(len(test_selection),1)
			else:
				test_selection = model_selection + data_frame[i_var]
				test_selection = test_selection.as_matrix().reshape(len(test_selection),1)

			X_train, X_test, y_train, y_test = train_test_split(test_selection,labels,test_size=0.1, random_state=seed)

			#print (X_train.shape)
			#print (y_train.shape)
			#print (X_test.shape)
			#print (y_test.shape)
			#quit()

			xg_train = xgboost.DMatrix(X_train, label=y_train)
			xg_test = xgboost.DMatrix(X_test, label=y_test)

			param = {}

			param['booster'] = 'gbtree'
			param['tree_method'] = 'auto'
			param['objective'] = 'binary:logistic'
			param['eta'] = 0.01
			param['max_depth'] = 6
			param['min_child_weight'] = 0.25
			param['subsample'] = 1.0
			param['silent'] = 1
			param['nthread'] = 3
			param['num_class'] = 1
			#param['base_score'] = 0.589

			#watchlist = [(xg_train, 'train'),(xg_test, 'test')]
			num_round = 100

			#model = xgboost.train(param, xg_train, num_round, watchlist)
			model = xgboost.train(param, xg_train, num_round)
			pred_prob = model.predict(xg_test).reshape(y_test.shape[0], 1)
			for i in range(len(pred_prob)):
				
				if pred_prob[i] >= 0.5:
					pred_prob[i] = 1
				else:
					pred_prob[i] = 0
			
			all_pred = 0
			correct_pred = 0
			for pred, label in zip(pred_prob, y_test):
				if pred[0] == label:
					correct_pred += 1
				all_pred += 1

			accuracy = correct_pred/all_pred
			#print ('VAR:', i_var, accuracy)

			if accuracy > accuracy_model and accuracy > accuracy_var:
				var_selection = i_var
				accuracy_var = accuracy

		if accuracy_var > accuracy_model:
			if first_var == True:
				model_selection = data_frame[var_selection]
			else:
				model_selection = model_selection + data_frame[var_selection]
			accuracy_model = accuracy_var

			model_list.append(var_selection)

		first_var = False
		print ('MODEL:', i_model, accuracy_model)
		print ('LIST:', model_list)
		print ('####################################')

	return None

def train_classifier_sklearn():

	seed = 24
	data = np.array(pickle.load(open('C:/NBA/data_games.pkl', 'rb')))	
	features = data[:,1:].astype(float)
	labels = data[:,0]
	X_train, X_test, y_train, y_test = train_test_split(features,labels,test_size=0.1, random_state=seed)
	
	# FEATURE SELECTION
	# CROSS VALIDATION
	# HYPER PARAMETER GRIDSEARCH
	# METHOD SELECTION
	# -> ensemble.			[AdaBoostClassifier, BaggingClassifier, ExtraTreesClassifier, GradientBoostingClassifier, RandomForestClassifier, VotingClassifier]
	# -> naive_bayes.		[BernoulliNB, GaussianNB, MultinomialNB]
	# -> neighbors.			[KNeighborsClassifier]
	# -> neural_network.	[MLPClassifier]
	# -> svm.				[LinearSVC, NuSVC, SVC]
	# -> tree.				[DecisionTreeClassifier, ExtraTreeClassifier]

	# AdaBoostClassifier
	########################################################################
	model_a = AdaBoostClassifier(			base_estimator=None,
											n_estimators=50, 
											learning_rate=1.0,
											algorithm='SAMME',
											random_state=seed)
	#model_a.fit(X_train, y_train)
	#print ('AdaBoostClassifier', model_a.score(X_test, y_test))
	########################################################################

	# BaggingClassifier
	########################################################################
	model_b = BaggingClassifier( 			base_estimator=None,
											n_estimators=10,
											max_samples=1.0,
											max_features=1.0,
											n_jobs=1,
											random_state=seed)
	#model_b.fit(X_train, y_train)
	#print ('BaggingClassifier', model_b.score(X_test, y_test))

	# ExtraTreesClassifier
	########################################################################
	model_c = ExtraTreesClassifier(			n_estimators=50, 
											max_features='auto',
											max_depth=None,
											min_samples_split=2,
											min_samples_leaf=1,
											min_weight_fraction_leaf=0.0,
											n_jobs=1,
											random_state=seed)
	#model_c.fit(X_train, y_train)
	#print ('ExtraTreesClassifier', model_c.score(X_test, y_test))
	########################################################################

	# GradientBoostingClassifier
	########################################################################
	model_d = GradientBoostingClassifier(	loss='deviance', 
											learning_rate=0.1,
											n_estimators=100,
											max_depth=3,
											min_samples_split=2,
											min_samples_leaf=1,
											min_weight_fraction_leaf=0.0,
											max_features=None,																				
											random_state=seed)
	#model_d.fit(X_train, y_train)
	#print ('GradientBoostingClassifier', model_d.score(X_test, y_test))
	########################################################################

	# RandomForestClassifier
	########################################################################
	model_e = RandomForestClassifier(		n_estimators=100, 
											max_features='auto',
											max_depth=3,
											min_samples_split=2,
											min_samples_leaf=1,
											min_weight_fraction_leaf=0.0,
											max_leaf_nodes=None,
											n_jobs=1,																				
											random_state=seed)
	#model_e.fit(X_train, y_train)
	#print ('RandomForestClassifier', model_e.score(X_test, y_test))
	########################################################################

	# LogisticRegression
	########################################################################
	model_f = LogisticRegression(			penalty='l2',
											random_state=seed,
											solver='liblinear',
											max_iter=100,
											n_jobs=1)
	#model_f.fit(X_train, y_train)
	#print ('LogisticRegression', model_f.score(X_test, y_test))
	########################################################################

	# SGDClassifier
	########################################################################
	model_g = SGDClassifier(				loss='log',
											penalty='l2',
											alpha=0.0001,
											n_iter=1000,
											shuffle=True,
											random_state=seed,
											learning_rate='optimal')
	#model_g.fit(X_train, y_train)
	#print ('SGDClassifier', model_g.score(X_test, y_test))
	########################################################################

	# BernoulliNB
	########################################################################
	model_h = BernoulliNB(					alpha=0.25,
											binarize=0.5,
											fit_prior=True,
											class_prior=None)
	#model_h.fit(X_train, y_train)
	#print ('BernoulliNB', model_h.score(X_test, y_test))
	########################################################################

	# GaussianNB
	########################################################################
	model_i = GaussianNB()

	#model_i.fit(X_train, y_train)
	#print ('GaussianNB', model_i.score(X_test, y_test))
	########################################################################

	# MultinomialNB
	########################################################################
	model_j = MultinomialNB(				alpha=1.0,
											fit_prior=True,
											class_prior=None)
	#model_j.fit(X_train, y_train)
	#print ('MultinomialNB', model_j.score(X_test, y_test))
	########################################################################

	# KNeighborsClassifier
	########################################################################
	model_k = KNeighborsClassifier(			n_neighbors=99,
											algorithm='brute',
											leaf_size=30,
											p=1,
											n_jobs=1)
	#model_k.fit(X_train, y_train)
	#print ('KNeighborsClassifier', model_k.score(X_test, y_test))
	########################################################################

	# MLPClassifier
	########################################################################
	model_l = MLPClassifier(				hidden_layer_sizes=(100,),
											activation='relu',
											solver='adam',
											alpha=0.0001,
											batch_size='auto',
											learning_rate='adaptive',
											max_iter=200,
											shuffle=True,
											random_state=seed)



	model_l.fit(X_train, y_train)
	print ('MLPClassifier', model_l.score(X_test, y_test))
	########################################################################

	# VotingClassifier
	########################################################################
	model = VotingClassifier(				estimators=[('model_a',model_a),
														('model_b',model_b),
														('model_c',model_c),
														('model_d',model_d),
														('model_e',model_e),
														('model_f',model_f),
														('model_g',model_g),
														('model_h',model_h),
														('model_i',model_i),
														('model_j',model_j),
														('model_k',model_k)], 
											voting='soft',
											n_jobs=1)
	#model.fit(X_train, y_train)
	#print ('VotingClassifier', model.score(X_test, y_test))
	########################################################################




	return None

def main():
	
	scrape_nba()

	# scrape, analyze, classify
	#state = 'analyze'			

	## LOADING BLOCK   ###############################################################################
	#form_list = [3,5,10,'all']
	#data, game_list = load_nba(state, form_list)
	##################################################################################################
	
	## SCRAPING BLOCK  ###############################################################################
	#n_team_list, max_team_list, min_player_list, max_player_list = get_lists(data)
	#for form in form_list:
	#	get_season_data(data, form, min_team_list, max_team_list, min_player_list, max_player_list)
	##################################################################################################

	## ANALYZER BLOCK  ###############################################################################	
	#game_list = create_game_list(game_list)
	#data = create_data(data, game_list)
	
	#print ('Data created')
	#with open('C:/NBA/data_games.pkl', 'wb') as f:
	#	pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
	#print ('Data saved')
	##################################################################################################
	
	## CLASSIFIER BLOCK ##############################################################################
	#train_classifier_xgboost()
	#train_classifier_sklearn()
	##################################################################################################


main()
