####################################################################################

PURPOSE:
To scrape team and player stats from NBA.com, for all games played within a specified period

OUTPUT:
a. A list of games played in the specified seasons. Containing an ID for the game, ID's for the teams, scores and result of the game
b. A dictionary containing team and player stats per game

INPUT NEEDED:
game_list_path:       Path to store a pickle containing the list of games played
data_path:            Path to store a pickle containing the dictionary of team and player stats
start_year:           Earliest season from which you want to retrieve data [2000 season is the earliest]
end_year:             Latest season
games_actual_season:  Number of games played so far, if you are in mid-season [otherwise insert 'default']

OUTPUT DICTIONARY:
The dictionary is built containing below levels:
-> season_ID
  -> team_ID
    -> player_ID or 'team_stats'
      -> game_ID
        -> a list of data on the player or the team for the specific game

####################################################################################
